import axios from 'axios';

export const quizzesListAPI = async () => {
  let response;
  try{
    response = await axios.get('quizzes/');
  } catch(err) {
    response = {"error": err.message};
  }
  return response;
}


export const quizDetailAPI = async (slug) => {
  let response;
  let instance = axios.create({
    baseURL: '/quizzes/', // if you don't specify leading slash, it will add current url to the beginning
  });
  try{
    response = await instance.get('/' + slug + '/'); // same here
  } catch(err){
    response = {"error": err.message, status: err.response.status};
  }
  return response;
}


export default quizzesListAPI;