function refresh_time() {
    var time = new Date();
    document.getElementById("time").textContent = time.toISOString();
}