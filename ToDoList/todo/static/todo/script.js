const url = new URL(document.URL)
let ID = url.pathname.split('/')[2]
let nextReqURL = `/api/todo/${ID}/?page=2&page_size=10`;
let commentSection = document.getElementById('comment-section')


function getComments() {
    if (nextReqURL !== '') {
        fetch(nextReqURL)
            .then(response => response.json())
            .then(data => {
                nextReqURL = data.comments.next
                for (const comment of data.comments.results) {
                    createHtmlCommend(comment)
                }
            })
            .catch(error => console.error(error))
    }else{
        console.log('sad')
    }
}
function createHtmlCommend(comment) {
    let htmlComment=
    `
    <div class="comment-title">
        <img class="comment-profile-pic" src="${comment['created_by']['profile_pic']}" alt="">
        <div class="comment-wrapper">
            <a href="${comment['created_by']['profile_web']}"><h3>${comment['created_by']['name']}</h3></a>
            <p>Commented on: ${comment['created_on']}</p>
        </div>
    </div>
    <p class="comment-text">${comment['text']}</p>
    `
    let commentDiv = document.createElement('div')
    commentDiv.className = "comment"
    commentDiv.innerHTML = htmlComment
    commentSection.appendChild(commentDiv)
            }

