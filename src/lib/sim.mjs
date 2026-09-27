/**
 * Математика мини-симулятора по лекциям 2 и 3: чистая логика без DOM.
 * Две задачи: лабиринт 3 × 4 (эпизодическая) и холодильник (непрерывная).
 * Лабиринт умеет работать в двух средах: детерминированной (тема 2, сносов нет) и
 * стохастической со сносами 0,8 / 0,1 / 0,1 (тема 3) — различие задаёт параметр slip.
 * Считаем доход G на трассе по стратегии ε-жадной и веса γ^k — ценности здесь не считаем.
 * Каждый шаг помнит, было ли действие случайным из-за ε (поле explored), — это для показа.
 */

/**
 * Генератор псевдослучайных чисел — чтобы прогон повторялся при одном и том же seed.
 * Сначала размешиваем seed (splitmix32): без этого у малых значений первые броски xorshift
 * смещены — например, при seed 1..999 первый бросок всегда попадал в диапазон до 0,1,
 * и при ε = 0,1 первый шаг каждого эпизода всегда оказывался случайным.
 */
export function makePrng(seed = 1) {
  let s = (seed >>> 0) || 1;
  s = (s + 0x9e3779b9) >>> 0;
  s = Math.imul(s ^ (s >>> 16), 0x21f0aaad) >>> 0;
  s = Math.imul(s ^ (s >>> 15), 0x735a2d97) >>> 0;
  s = (s ^ (s >>> 15)) >>> 0;
  return () => {
    s ^= s << 13;
    s >>>= 0;
    s ^= s >>> 17;
    s ^= s << 5;
    s >>>= 0;
    return s / 4294967296;
  };
}

/** Эффективный горизонт: при γ = 1 он бесконечен. */
export const horizon = (gamma) => (gamma >= 1 ? Infinity : 1 / (1 - gamma));

/** Веса будущих вознаграждений: γ^0, γ^1, … γ^(n−1). */
export function weights(gamma, n) {
  const out = [];
  let w = 1;
  for (let k = 0; k < n; k += 1) {
    out.push(w);
    w *= gamma;
  }
  return out;
}

/**
 * ε-жадный выбор: с вероятностью ε — случайное действие, иначе лучшее известное.
 * Возвращает { action, explored }: explored = true — действие выбрано случайно из-за ε.
 * Броски генератора остаются те же и в том же порядке, что и раньше, поэтому прогоны не меняются.
 */
export function epsilonGreedy(best, actions, epsilon, rnd) {
  if (rnd() < epsilon) {
    return { action: actions[Math.floor(rnd() * actions.length)], explored: true };
  }
  return { action: best, explored: false };
}

/* ---------- Лабиринт 3 × 4 (эпизодическая задача) ---------- */

export const MAZE = { rows: 3, cols: 4, cells: 12, exit: 12 };
export const MAZE_ACTIONS = ['Вверх', 'Вниз', 'Влево', 'Вправо'];

const OFFSETS = { Вверх: [-1, 0], Вниз: [1, 0], Влево: [0, -1], Вправо: [0, 1] };

const posOf = (id) => ({ r: Math.floor((id - 1) / MAZE.cols), c: (id - 1) % MAZE.cols });
const idOf = (r, c) => r * MAZE.cols + c + 1;

function move(id, action) {
  const { r, c } = posOf(id);
  const [dr, dc] = OFFSETS[action];
  const nr = r + dr;
  const nc = c + dc;
  if (nr < 0 || nr >= MAZE.rows || nc < 0 || nc >= MAZE.cols) return id; // стенка — остаёмся на месте
  return idOf(nr, nc);
}

/**
 * Вероятность того, что команда сработает как задумано.
 * SLIP_LECTURE3 = 0,8 — среда лекции 3: с p = 0,8 команда срабатывает, по 0,1 снос уводит вбок.
 * SLIP_DETERMINISTIC = 1 — детерминированная среда: команда срабатывает всегда, сносов нет.
 */
export const SLIP_LECTURE3 = 0.8;
export const SLIP_DETERMINISTIC = 1;

/** Куда уводит снос: движение вбок относительно задуманной команды. */
const SLIPS = {
  Вправо: ['Вверх', 'Вниз'],
  Влево: ['Вверх', 'Вниз'],
  Вверх: ['Влево', 'Вправо'],
  Вниз: ['Влево', 'Вправо'],
};

/**
 * Расстояние до выхода по клеткам (BFS) — используется как «лучшее известное» действие.
 * Считаем строго ОТ ВЫХОДА: расстояния и «лучшее известное» действие от старта не зависят,
 * поэтому старт здесь не параметр — не переписывай «от старта».
 */
export function mazeDistanceToExit() {
  const dist = new Array(MAZE.cells + 1).fill(Infinity);
  dist[MAZE.exit] = 0;
  const queue = [MAZE.exit];
  while (queue.length > 0) {
    const id = queue.shift();
    for (const action of MAZE_ACTIONS) {
      const from = move(id, flip(action));
      if (from === id) continue;
      if (dist[from] > dist[id] + 1) {
        dist[from] = dist[id] + 1;
        queue.push(from);
      }
    }
  }
  return dist;
}

const flip = (action) => ({ Вверх: 'Вниз', Вниз: 'Вверх', Влево: 'Вправо', Вправо: 'Влево' })[action];

/** «Лучшее известное» действие в клетке: шаг, сокращающий расстояние до выхода. */
export function mazeBestAction(id, dist) {
  let best = MAZE_ACTIONS[0];
  let bestDist = Infinity;
  for (const action of MAZE_ACTIONS) {
    const next = move(id, action);
    const d = next === id ? Infinity : dist[next];
    if (d < bestDist) {
      bestDist = d;
      best = action;
    }
  }
  return best;
}

/**
 * Исходы одного шага в клетке id: как задумано, снос 1, снос 2 — ровно в этом порядке.
 * prob — вероятность исхода: у команды slip, у каждого сноса (1 − slip) / 2; сумма по массиву
 * ровно 1 (проверено для всех p шага 0,05). to — клетка после хода, если ход упёрся в стенку —
 * та же клетка и stay = true. slipped — сработала ли команда не как задумано.
 * При slip = 1 сносов нет: единственный исход с prob = 1.
 * Здесь только модель среды (вероятности p(s′ | s, a)), без бросков генератора.
 */
export function mazeOutcomes(id, action, slip = SLIP_LECTURE3) {
  const planned = move(id, action);
  const out = [{ prob: slip, to: planned, slipped: false, stay: planned === id }];
  if (slip < 1) {
    const side = (1 - slip) / 2;
    for (const dir of SLIPS[action]) {
      const to = move(id, dir);
      out.push({ prob: side, to, slipped: true, stay: to === id });
    }
  }
  return out;
}

/**
 * Один шаг лабиринта: каждый шаг стоит stepReward; вход в выход завершает эпизод, а «награда за
 * выход» приходит не в этом шаге, а отдельным терминальным членом — её вклад в доход идёт с весом
 * γ^N, где N — число шагов до выхода (как в теме 3: три награды −1 с весами 1, γ, γ² и +10 с весом
 * γ³). Поэтому сам шаг в выход начисляет только stepReward, а exitReward возвращается полем bonus —
 * его добавляет runMaze. Иначе +10 посчитался бы дважды: один раз в шаге, второй — через v(выхода).
 * slip — вероятность, что команда сработает как задумано; slip = 1 — детерминированная среда.
 * Возвращает новую клетку, награду за шаг, терминальную награду за выход (bonus) и признак конца.
 * Модель берём из mazeOutcomes, а бросок делаем по ней: бросок «сработала ли команда» — ВСЕГДА и
 * до ветвления, второй бросок (направление сноса) — только когда снос случился. Порядок и число
 * бросков те же, что были у прежней версии с жёстким порогом 0,8, поэтому прогоны совпадают.
 */
export function mazeStep(id, action, stepReward, exitReward, rnd, slip = SLIP_LECTURE3) {
  const outcomes = mazeOutcomes(id, action, slip);
  const roll = rnd();
  // исход «как задумано» занимает первый отрезок [0, slip); остальное — сносы, их ровно два
  const chosen = roll >= outcomes[0].prob ? (rnd() < 0.5 ? outcomes[1] : outcomes[2]) : outcomes[0];
  const next = chosen.to;
  const done = next === MAZE.exit;
  return { next, reward: stepReward, bonus: done ? exitReward : 0, done, slipped: chosen.slipped };
}

/**
 * Ценности клеток «по расстоянию до выхода» — как в лекции 3: шаг считаем без сносов, поэтому
 * ценность зависит только от расстояния d до выхода: v(0) = exitReward (это выход),
 * v(d) = stepReward + γ · v(d − 1). Возвращает массив v[1..12] (индекс 0 не используется).
 * Для γ = 0,9, stepReward = −1, exitReward = +10 выходит 10,00 → 8,00 → 6,20 → 4,58 → 3,12 → 1,81.
 * Это не истинные ценности задачи (те считаются на лекции 5), а оценка по расстоянию.
 * Ту же модель награды использует runMaze: шаг стоит stepReward, а «награда за выход» входит с весом
 * γ^N (N — число шагов до выхода), поэтому детерминированный прогон даёт ровно эти v(старт).
 */
export function mazeDistanceValues({ gamma, stepReward, exitReward }) {
  const dist = mazeDistanceToExit();
  let maxDist = 0;
  for (let id = 1; id <= MAZE.cells; id += 1) {
    if (Number.isFinite(dist[id]) && dist[id] > maxDist) maxDist = dist[id];
  }
  const byDist = [exitReward];
  for (let d = 1; d <= maxDist; d += 1) byDist[d] = stepReward + gamma * byDist[d - 1];
  const v = new Array(MAZE.cells + 1).fill(0);
  for (let id = 1; id <= MAZE.cells; id += 1) {
    v[id] = Number.isFinite(dist[id]) ? byDist[dist[id]] : 0; // недостижимых клеток тут нет
  }
  return v;
}

/**
 * Прогон одного эпизода лабиринта по ε-жадной стратегии.
 * start — стартовая клетка (по умолчанию S1); если старт совпал с выходом, эпизод пустой.
 * slip — вероятность срабатывания команды: 0,8 (лекция 3) или 1 (детерминированная среда, тема 2).
 * Доход считаем по модели темы 3: каждый шаг даёт stepReward, а пришедший в выход «бонус за выход»
 * добавляется один раз, с весом γ^N (N — число шагов до выхода), поэтому в детерминированной среде
 * итоговый G совпадает с mazeDistanceValues (ценностью «по расстоянию»).
 */
export function runMaze({
  gamma,
  epsilon,
  stepReward,
  exitReward,
  maxSteps = 200,
  seed = 1,
  start = 1,
  slip = SLIP_LECTURE3,
}) {
  if (start === MAZE.exit) return { steps: [], g: 0, done: true, stepsCount: 0, start };
  const rnd = makePrng(seed);
  const dist = mazeDistanceToExit();
  const steps = [];
  let id = start;
  let g = 0;
  let discount = 1;
  let done = false;
  for (let t = 0; t < maxSteps && !done; t += 1) {
    const best = mazeBestAction(id, dist);
    const choice = epsilonGreedy(best, MAZE_ACTIONS, epsilon, rnd);
    const action = choice.action;
    const outcome = mazeStep(id, action, stepReward, exitReward, rnd, slip);
    g += discount * outcome.reward;
    // «награда за выход» — отдельным терминальным членом с весом γ^(t + 1) = γ^N (N — шагов до выхода)
    if (outcome.done) g += discount * gamma * outcome.bonus;
    steps.push({
      t,
      from: id,
      to: outcome.next,
      action,
      reward: outcome.reward,
      bonus: outcome.bonus,
      g,
      slipped: outcome.slipped,
      explored: choice.explored,
      done: outcome.done,
    });
    discount *= gamma;
    id = outcome.next;
    done = outcome.done;
  }
  return { steps, g, done, stepsCount: steps.length, start };
}

/* ---------- Холодильник (непрерывная задача) ---------- */

export const FRIDGE = { target: 4, ambient: 22, min: -2, max: 26 };
export const FRIDGE_ACTIONS = ['Сильнее', 'Слабее', 'Ничего'];
const COOLING = { Сильнее: -1, Слабее: -0.4, Ничего: 0 };

/** Следующая температура и вознаграждение за шаг (штраф за отклонение от цели). */
export function fridgeStep(temp, action, penalty = 1, k = 0.03) {
  const next = Math.min(
    FRIDGE.max,
    Math.max(FRIDGE.min, temp + k * (FRIDGE.ambient - temp) + COOLING[action])
  );
  return { next, reward: -penalty * Math.abs(next - FRIDGE.target) };
}

/** «Лучшее известное» действие: то, после которого температура ближе всего к цели. */
export function fridgeBestAction(temp, penalty = 1) {
  let best = FRIDGE_ACTIONS[0];
  let bestReward = -Infinity;
  for (const action of FRIDGE_ACTIONS) {
    const { reward } = fridgeStep(temp, action, penalty);
    if (reward > bestReward) {
      bestReward = reward;
      best = action;
    }
  }
  return best;
}

/**
 * Прогон непрерывной задачи: N шагов, конца нет.
 * converged — прирост дохода за последние 20 шагов почти нулевой: сумма сходится.
 */
export function runFridge({ gamma, epsilon, penalty = 1, steps: total = 120, seed = 1 }) {
  const rnd = makePrng(seed);
  const steps = [];
  let temp = FRIDGE.ambient;
  let g = 0;
  let discount = 1;
  for (let t = 0; t < total; t += 1) {
    const best = fridgeBestAction(temp, penalty);
    const choice = epsilonGreedy(best, FRIDGE_ACTIONS, epsilon, rnd);
    const action = choice.action;
    const { next, reward } = fridgeStep(temp, action, penalty);
    g += discount * reward;
    steps.push({ t, temp: next, action, reward, g, explored: choice.explored });
    discount *= gamma;
    temp = next;
  }
  const tail = steps.slice(-20);
  const growth = tail.reduce(
    (sum, step, index) => sum + Math.pow(gamma, total - 20 + index) * step.reward,
    0
  );
  return { steps, g, temp, converged: Math.abs(growth) < 0.1, growth };
}
