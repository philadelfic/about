// Задания курса: порядок и подписи — в одном месте, чтобы список в навигации,
// список на странице заданий и обратная ссылка «тема → задания» не расходились.

/** Порядок — по номеру в имени файла (01, 02, …): он же порядок выдачи заданий. */
export const homeworkOrder = (item) => Number.parseInt(String(item.id), 10) || 0;

/** Подпись для навигации: сначала «по лекции», потом «к семинару», потом «по теме». */
export const homeworkLabel = (item) => {
  const { lecture, seminar, topic, title } = item.data;
  if (lecture) return `ДЗ по лекции ${lecture}`;
  if (seminar) return `ДЗ к семинару ${seminar}`;
  if (topic) return `ДЗ по теме ${topic}`;
  return title;
};

/** Короткая надпись для списков: «Лекция 4» / «К семинару 2» / «К теме 3». */
export const homeworkKind = (item) => {
  const { lecture, seminar, topic } = item.data;
  if (lecture) return `Лекция ${lecture}`;
  if (seminar) return `К семинару ${seminar}`;
  if (topic) return `К теме ${topic}`;
  return 'Задание';
};
