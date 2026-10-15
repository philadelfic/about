/**
 * Тесты математики симулятора (src/lib/sim.mjs) — раннер встроен в Node: node --test tests/.
 * Здесь живут инварианты, которые раньше существовали только комментариями в коде
 * («сумма вероятностей ровно 1», «детерминированный прогон даёт ценность по расстоянию»).
 */
import test from 'node:test';
import assert from 'node:assert/strict';

import {
  horizon,
  weights,
  makePrng,
  epsilonGreedy,
  mazeOutcomes,
  mazeDistanceValues,
  runMaze,
  fridgeStep,
  fridgeBestAction,
  runFridge,
  MAZE,
  MAZE_ACTIONS,
  FRIDGE,
  SLIP_LECTURE3,
  SLIP_DETERMINISTIC,
} from '../src/lib/sim.mjs';

const near = (actual, expected, epsilon = 1e-9, message = '') =>
  assert.ok(
    Math.abs(actual - expected) < epsilon,
    `${message}: ждали ≈${expected}, получили ${actual}`
  );

test('horizon: 1/(1−γ), при γ = 1 — бесконечность', () => {
  near(horizon(0.9), 10);
  near(horizon(0.5), 2);
  assert.equal(horizon(1), Infinity);
});

test('weights: γ^0, γ^1, … γ^(n−1)', () => {
  const w = weights(0.9, 3);
  assert.equal(w.length, 3);
  assert.equal(w[0], 1);
  near(w[1], 0.9);
  near(w[2], 0.81);
});

test('makePrng: один seed — одна последовательность', () => {
  const a = makePrng(42);
  const b = makePrng(42);
  const c = makePrng(43);
  const seqA = [a(), a(), a()];
  const seqB = [b(), b(), b()];
  assert.deepEqual(seqA, seqB);
  assert.notDeepEqual(seqA, [c(), c(), c()]);
  for (const value of [...seqA, ...seqB]) {
    assert.ok(value >= 0 && value < 1, `бросок вне [0, 1): ${value}`);
  }
});

test('epsilonGreedy: при ε = 0 случайных действий нет, при ε = 1 — всегда случайное', () => {
  let calls = 0;
  const rnd = () => {
    calls += 1;
    return 0.999;
  };
  // бросок за ε делается всегда (стабильный порядок бросков), но при ε = 0 он ничего не меняет
  const best = epsilonGreedy('Вверх', MAZE_ACTIONS, 0, rnd);
  assert.deepEqual(best, { action: 'Вверх', explored: false });
  assert.equal(calls, 1);

  const random = epsilonGreedy('Вверх', MAZE_ACTIONS, 1, rnd);
  assert.equal(random.explored, true);
  // rnd = 0.999 → индекс floor(0.999 · 4) = 3 — последнее действие списка
  assert.equal(random.action, MAZE_ACTIONS[3]);
  assert.equal(calls, 3);
});

test('mazeOutcomes: сумма вероятностей ровно 1, исходы в границах поля', () => {
  for (let slip = 0.5; slip <= 1.0001; slip += 0.05) {
    for (let cell = 1; cell <= MAZE.cells; cell += 1) {
      for (const action of MAZE_ACTIONS) {
        const outcomes = mazeOutcomes(cell, action, slip);
        const sum = outcomes.reduce((acc, o) => acc + o.prob, 0);
        near(sum, 1, 1e-12, `slip=${slip}, S${cell}, ${action}`);
        for (const o of outcomes) {
          assert.ok(o.to >= 1 && o.to <= MAZE.cells, `клетка-исход вне поля: ${o.to}`);
          assert.equal(o.slipped, o !== outcomes[0]);
        }
      }
    }
  }
});

test('mazeOutcomes: при slip = 1 сносов нет — единственный исход', () => {
  const outcomes = mazeOutcomes(5, 'Вверх', SLIP_DETERMINISTIC);
  assert.equal(outcomes.length, 1);
  assert.equal(outcomes[0].prob, 1);
  assert.equal(outcomes[0].slipped, false);
});

test('mazeOutcomes: снос уводит вбок от задуманной команды', () => {
  // клетка 6 (в центре поля): задумано Вверх (клетка 2), сносы — Влево (5) и Вправо (7)
  const outcomes = mazeOutcomes(6, 'Вверх', SLIP_LECTURE3);
  assert.deepEqual(
    outcomes.map((o) => o.to),
    [2, 5, 7]
  );
  near(outcomes[0].prob, 0.8);
  near(outcomes[1].prob, 0.1);
  near(outcomes[2].prob, 0.1);
});

// В детерминированной среде ε-жадная стратегия с ε = 0 каждый шаг сокращает расстояние
// до выхода, поэтому доход прогона обязан совпасть с ценностью «по расстоянию» —
// это главный инвариант из комментариев runMaze и mazeDistanceValues.
test('runMaze (slip=1, ε=0): доход прогона совпадает с ценностью по расстоянию', () => {
  for (const gamma of [0.9, 0.5, 0.7, 1]) {
    for (const [stepReward, exitReward] of [
      [-1, 10],
      [-1, 20],
      [-0.5, 5],
      [-3, 10],
    ]) {
      const run = runMaze({ gamma, epsilon: 0, stepReward, exitReward, seed: 7, start: 1, slip: 1 });
      const values = mazeDistanceValues({ gamma, stepReward, exitReward });
      assert.ok(run.done, `эпизод должен закончиться: γ=${gamma}`);
      near(run.g, values[1], 1e-9, `γ=${gamma}, r=${stepReward}, выход=${exitReward}`);
    }
  }
});

test('runMaze: старт с выхода — эпизод пустой', () => {
  const run = runMaze({ gamma: 0.9, epsilon: 0.1, seed: 7, start: MAZE.exit, slip: SLIP_LECTURE3 });
  assert.deepEqual(run, { steps: [], g: 0, done: true, stepsCount: 0, start: MAZE.exit });
});

test('runMaze: воспроизводимость — один seed, один прогон', () => {
  const params = { gamma: 0.9, epsilon: 0.1, seed: 123, start: 3, slip: SLIP_LECTURE3 };
  const a = runMaze(params);
  const b = runMaze(params);
  assert.deepEqual(a, b);
});

test('fridgeStep: шаг к цели и штраф за отклонение', () => {
  const { next, reward } = fridgeStep(22, 'Сильнее', 1);
  near(next, 21);
  near(reward, -17); // −|21 − 4|
  const clamped = fridgeStep(FRIDGE.min, 'Сильнее', 2);
  assert.equal(clamped.next, FRIDGE.min); // ниже минимума не уходим
});

test('fridgeBestAction: из комнатной температуры strongest охлаждение', () => {
  assert.equal(fridgeBestAction(22, 1), 'Сильнее');
});

test('runFridge: при γ < 1 сумма сходится, при γ = 1 — нет', () => {
  const converging = runFridge({ gamma: 0.9, epsilon: 0.1, seed: 7 });
  assert.equal(converging.steps.length, 120);
  assert.equal(converging.converged, true);
  assert.ok(converging.g < 0, `доход непрерывной задачи отрицательный: ${converging.g}`);

  const diverging = runFridge({ gamma: 1, epsilon: 0.1, seed: 7 });
  assert.equal(diverging.converged, false);
});
