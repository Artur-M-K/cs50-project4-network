const likeButtons = document.querySelectorAll('#like');
// const likes = document.querySelector('.post-body-likes');

// likeButtons.forEach(button => {
//     button.addEventListener('click', () => {
//         console.log('dziala', button.dataset.id);
//         fetch(`/like/${button.dataset.id}`)
//         .then(response => response.json())
//         .then(data => {
        
//             console.log(data)

        
//         });
        
//     })
// })

likeButtons.forEach(button => {
    button.addEventListener('click', () => likePost(button.value))
})

function likePost(id) {
    const likes = document.querySelectorAll(`[data-id="${id}"]`);
    console.log(likes)
    fetch(`/like/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            like: true
        })
    });
    fetch(`/like/${id}`)
            .then(response => response.json())
            .then(post => {
              console.log(post.likes)
              likes[0].innerHTML = 'Likes: ' + post.likes
            });
   
}