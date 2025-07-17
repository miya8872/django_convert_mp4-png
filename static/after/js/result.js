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
    const csrftoken = getCookie('csrftoken')

    function progress(){
        fetch(urls.progress, {
            method: "POST",
            body: JSON.stringify(object_id),
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
                'X-CSRFToken': csrftoken,
            },
        }).then(response => response.text())
        .then(text => {
            if(text){
                let num = parseFloat(text);
                if(num == -1.00){
                    document.getElementById("progress").textContent = ":--------------------: 待機中";
                    getImg(urls.img,"waiting",csrftoken);
                }
                if(num == 100.00){
                    document.getElementById("progress").textContent = ":====================: 完了";
                    getImg(urls.img,"result",csrftoken,object_id);
                }
                if(num < 100.00 && num >= 0.00){
                    let str = ":";
                    pro = Math.round(num/5)*5;
                    for (let i = 0; i < 100; i+=5){
                        if(pro > i){str+="=";}
                        else{str+="-";}
                    }
                    str+= ": " + text + "%";
                    document.getElementById("progress").textContent = str;
                    getImg(urls.img,"progressing",csrftoken);
                }
            }
        });
    }
    progress();
    setInterval(progress, 2000);
});
