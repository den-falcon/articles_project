let articleButtons = document.getElementsByName('article-like')
let commentButtons = document.getElementsByName('comment-like')

async function likeOrUnlike(event, method='POST') {
    let eventTarget = event.target;
    let url = eventTarget.dataset.requestUrl;
    let elementId = eventTarget.dataset.elementId;
    let csrf = document.cookie.match(/csrftoken=([\w-]+)/)[1];
    let request = new Request(url, {headers: {'X-CSRFToken': csrf}});
    let response;
    if (eventTarget.dataset.isLiked === 'false') {
        response = await fetch(request, {method});
    } else {
        method = 'DELETE'
        response = await fetch(request, {method});
    }

    if (response.ok) {
        let responseBody = await response.json();
        let totalElement = document.getElementById(elementId);
        if (responseBody['is_fan']) {
            eventTarget.innerText = 'Дизлайк';
        } else {
            eventTarget.innerText = 'Лайк';
        }
        eventTarget.dataset.isLiked = responseBody['is_fan'];
        totalElement.innerText = responseBody['total_likes'];
        return responseBody;
    }
}


window.addEventListener('load', function() {
    for (let i=0; i<articleButtons.length; i++) {
            articleButtons[i].addEventListener('click', likeOrUnlike)
    }
    for (let i=0; i<commentButtons.length; i++) {
        commentButtons[i].addEventListener('click', likeOrUnlike)
    }
})