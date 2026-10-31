// Руководства курса: порядок и подписи — в одном месте, как у заданий и тем.

/** Порядок — по полю order, а если его нет — по номеру в имени файла. */
export const guideOrder = (item) => {
  if (typeof item.data?.order === 'number') return item.data.order;
  return Number.parseInt(String(item.id), 10) || 0;
};

/** Короткая надпись для списка: «Семинар 4» или «Руководство». */
export const guideKind = (item) => (item.data?.seminar ? `Семинар ${item.data.seminar}` : 'Руководство');
