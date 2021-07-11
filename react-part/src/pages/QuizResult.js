import axios from 'axios';
import React, {useEffect, useState} from 'react'
import QuestionMS from '../components/QuestionMS';
import QuestionSS from '../components/QuestionSS';
import QuestionText from '../components/QuestionText';

export default function QuizResult(props) {
  const [results, setResults] = useState([]);

  const slug = props.match.params.slug;

  useEffect(() => {
    axios
      .get(`/api/quizzes/${slug}/results/`)
      .then(data => {
        setResults(data.data);
      })
      .catch(console.log)
      
  }, [slug])

  if (results.length === 0){
    return <h1>Loading!</h1>
  }

  return (
    <div className="quiz-question">
      <div className="chat"></div>
      <main>
        {results.map(result => {
          if (result.variant === 'SS'){
            return <QuestionSS
              key={result.id}
              question={result}
              choice={+Object.values(result['user_answer'][0])[0]}
              isResult={true}
            />
          } else if (result.variant === 'MS'){
            return <QuestionMS
              key={result.id}
              question={result}
              choices={result['user_answer'].map(ans => Object.values(ans)[0])}
              isResult={true}
            />
          } else if (result.variant === 'T'){
            return <QuestionText 
              key={result.id}
              question={result}
              answer={result['user_answer'][0]}
              isResult={true}
            />
          }
        })}
      </main>
    </div>
  )
}
