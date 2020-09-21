const get = async url => {
    const response = await fetch(url);
    const res = await response.json();
    return res
}

const populateVideoList = videos => {
    const videoOptions = videos.map(v => `<option>${v}</option>`).join();
    $('#videoSelect').html(videoOptions).selectpicker('refresh');
}

const run = async () => {
    const videos = await get('/get_available_videos');
    populateVideoList(videos);

    $('#startBtn').click(() => {
        $('#startBtn').prop('disabled', true);
        const videoStreamer = new VideoStreamer();
        videoStreamer.start();
    });
}

run();

