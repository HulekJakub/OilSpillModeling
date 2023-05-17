
const updatePath = 'http://127.0.0.1:5000/check';
const div = document.querySelector('div');
setInterval(() => {
    fetch(updatePath, {headers: {Accept: 'application/json'}})
    .then(async (response) => {
        const body = await response.json();
        div.innerText = body['a']
    });

}, 1000);
