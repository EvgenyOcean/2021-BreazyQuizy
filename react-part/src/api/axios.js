import axios from 'axios';


async function handleTokenRefresh(){
  console.log('handling...');
} 


export const quizzesListAPI = async () => {
  let response;
  try{
    response = await axios.get('/api/quizzes/');
  } catch(err) {
    response = {"error": err.message};
  }
  return response;
}


export const quizDetailAPI = async (slug) => {
  let response;
  let accessToken = localStorage.getItem('access');
  let instance = axios.create({
    baseURL: '/api/quizzes/', 
    headers: {'Authorization': accessToken ? 'Bearer ' +  accessToken : ''},
  });
  try{
    response = await instance.get('/' + slug + '/');
  } catch(err){
    if (err.response.status === 401){
      await handleTokenRefresh();
    }
    console.log('error!');
    response = {"error": err.message, status: err.response.status};
  }
  return response;
}


export const RegisterAPI = async (data) => {
  return await axios.post('/register/', data);
}


export const LoginAPI = async (data) => {
  return await axios.post('/login/', data);
}


export const LogoutAPI = async () => {
  const refresh = localStorage.getItem('refresh');
  localStorage.removeItem('refresh');
  localStorage.removeItem('access');
  return await axios.post('/logout/', {refresh})
}


export default quizzesListAPI;