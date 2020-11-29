import { LoginAPI, RegisterAPI} from './api/axios';

export const parseJwt = (token) => {
    let base64Url = token.split('.')[1];
    let base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    let jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));

    return JSON.parse(jsonPayload);
};

export const handleFormSubmit = async (action, e) => {
  e.preventDefault();
  const data = new FormData(e.target);
  let result;
  try{
    if (action === 'login'){
      let response = await LoginAPI(data);
      const {access, refresh} = response.data;
      localStorage.setItem('refresh', refresh);
      localStorage.setItem('access', access);
    } else if (action === 'register'){
      await RegisterAPI(data);
    }
    result = 'success'
  } catch (err){
    if (err.response.status === 400 || err.response.status === 401){
      if (action === 'login'){
        document.querySelectorAll('.login-error').forEach(el => {el.remove()});
        let containerDiv = document.forms[0].parentElement;
        let div = document.createElement('div');
        div.classList.add('alert-danger', 'alert', 'my-3', 'login-error');
        div.textContent = err.response.data.detail;
        containerDiv.prepend(div);
      } else {
        const errData = err.response.data;
        console.log(errData);
        document.querySelectorAll('input').forEach(el => {el.style.border = '2px solid green'});
        document.querySelectorAll('small').forEach(small => small.remove());
        Object.getOwnPropertyNames(errData).forEach(errFieldName => {
          let formFieldEl = document.forms[0].querySelector(`[name=${errFieldName}]`);
          formFieldEl.style.border = "1px solid red";
          let small = document.createElement('small');
          small.style.color = 'red';
          small.textContent = errData[errFieldName][0];
          formFieldEl.after(small);
        })
      }
    }
    result = 'error';
  } finally {
    return result;
  }
}

export default handleFormSubmit;