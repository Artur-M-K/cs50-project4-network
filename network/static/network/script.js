
const getData = () => {
    console.log('dziala')
    fetch('followers', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        result = response.json()
        return result;
    })
    .then(result => {
        console.log(result)
    })
}

document.querySelector('.add').addEventListener('click', getData);
