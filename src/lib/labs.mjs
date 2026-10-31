// Лабораторные работы: порядок и подписи — в одном месте, как у заданий и тем.

/** Порядок — по номеру работы, а если его нет — по номеру в имени файла. */
export const labOrder = (item) => {
  if (typeof item.data?.number === 'number') return item.data.number;
  return Number.parseInt(String(item.id), 10) || 0;
};

/** Короткая надпись для списка: «Лабораторная 2». */
export const labKind = (item) => `Лабораторная ${item.data?.number ?? ''}`.trim();
