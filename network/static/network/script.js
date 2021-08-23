
function likePost(id) {
  
    const likes = document.querySelectorAll(`[data-id="${id}"]`);
    console.log(likes[0].innerHTML)
    
    fetch(`/like/${id}`)
            .then(response => response.json())
            .then(post => {
                console.log(post)
              if (post.isLiked == false) {
                fetch(`/like/${id}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        isLiked: true,
                        like: true
                    })
                });
                likes[0].innerHTML = 'Likes: ' + post.likes;
                const btn = document.getElementById(`like${id}`)
                console.log(btn)
                btn.innerHTML = 'Unlike'
              }
              if (post.isLiked == true){
                fetch(`/like/${id}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        isLiked: false,
                        like: false
                    })
                    
                });
                likes[0].innerHTML = 'Likes: ' + post.likes;
                const btn = document.getElementById(`like${id}`)
                btn.innerHTML = 'Like'
              }
              // location.reload();
            });
            
}