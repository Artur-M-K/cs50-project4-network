
$('.like-form').submit(function(e){
  e.preventDefault()

  const post_id = $(this).attr('id')
  const likeText = $(`.like-btn${post_id}`).text()
  const trim = $.trim(likeText)

  const url = $(this).attr('action')
  console.log(trim)

  let res;
  const likes = $(`.like-count${post_id}`).text()
  const trimCount = parseInt(likes)
  console.log(trimCount, likes)
  $.ajax({
    type: 'POST',
    url: url,
    data: {
      'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
      'post_id':post_id,
    },
    success: function(response) {
      console.log('success', response)
      if(trim === 'Unlike') {
        $(`.like-btn${post_id}`).text('Like')
        res = trimCount - 1
      }else{
        $(`.like-btn${post_id}`).text('Unlike')
        res = trimCount + 1
      }

      $(`.like-count${post_id}`).text(res)
    },
    error: function(response) {
      console.log('error', response)
    }
  })
})