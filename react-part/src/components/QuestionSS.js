import React from 'react';
import classnames from 'classnames';

export default function QuestionSS(props) {
  const question = props.question;
  const isResult = props.isResult;

  return (
    <div className='question'>
      <h3 className="question-title">{question.title}</h3>
      <div className="choices">
        {question.choices.map((c) => (
          <div
            key={c.id}
            className={classnames('choice', {'correct': c['is_correct'] && isResult}, {'wrong': c.id === props.choice && !c['is_correct'] && isResult})}
            data-choice-id={c.id}
            {...(!isResult ? {'onClick': (e) => props.handleChoiceClick(e.target)} : () => {})}
          >
            <div className="circle">
              {c.id === props.choice && <div className="inner-circle"></div>}
            </div>
            <div className="choice-ss">{c.title}</div>
          </div>
        ))}
      </div>
    </div>
  )
}
