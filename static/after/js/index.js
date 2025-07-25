document.addEventListener("DOMContentLoaded", function(){
    const getCookie = (name) => {
        if(document.cookie && document.cookie !== '') {
            for(const cookie of document.cookie.split(';')) {
                const [key, value] = cookie.trim().split('=')
                if(key === name) {
                    return decodeURIComponent(value)
                }
            }
        }
    }
    const csrftoken = getCookie('csrftoken');
    getImg(urls.img,"example",csrftoken);
    setInterval(progress, 20000);
});
