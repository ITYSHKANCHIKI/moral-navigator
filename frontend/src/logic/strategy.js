// frontend/src/logic/strategy.js
export class SimpleScoreStrategy {
  calculate (answers) {
    const sum   = answers.reduce((s,a)=>s + (a.score ?? 0), 0)
    const max   = answers.length
    const ratio = sum / max
    let text

    if (ratio > 0.5) {
      text = 'Вы сделали утилитарный выбор: спасение жизни важнее соблюдения закона.'
    } else {
      text = 'Вы придерживаетесь деонтологического подхода: закон важнее результата.'
    }

    return { sum, max, text }
  }
}

export function getStrategy () {
  return new SimpleScoreStrategy()
}
