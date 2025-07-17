function menu() {
    const menu = document.getElementById("base_dropdown");
    menu.classList.toggle("base_hidden");
}

function copyId(){
    navigator.clipboard.writeText(object_id).then(() => {
        alert("IDをコピーしました。");
    }).catch(e => {
        alert("IDのコピーに失敗しました: " + e);
    });
}

function getImg(url,purpose,csrftoken,id="None"){
    fetch(url, {
        method: "POST",
        body: JSON.stringify({
            purpose: purpose,
            id: id
        }),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
    }).then(response => response.json())
    .then(data => {
        const base64 = data.img_base64;

        const img = document.createElement("img");
        img.src = `data:image/png;base64,${base64}`;
        img.alt = "Base64で受け取った画像";
        img.style.maxWidth = "1920px";

        const container = document.getElementById("img_container");
        container.innerHTML = '';
        container.appendChild(img);
    })
    .catch(error => {
        console.error("画像の取得に失敗しました:", error);
        document.getElementById("img_container").textContent = "画像の取得に失敗しました";
    });
}
