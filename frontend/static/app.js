const evtSource = new EventSource('/generate_predictions?video_name=test_clip.15s.mp4');

const plotFig = (imgUrl) => {
    const trace1 = {
        source: imgUrl,
        type: 'image'
    };

    const layout = {
        width: 1024,
        height: 1024
    };

    const plotExists = $('#plot.js-plotly-plot').length > 0;

    if(plotExists) {
        Plotly.restyle('plot', {source: [trace1.source]});
    } else {
        Plotly.newPlot('plot', [trace1], layout);
    }


};

const get = async (url, settings) => {
    const response = await fetch(url, settings);
    const res = await response.blob();
    return res
}

evtSource.onmessage = async e => {
    const res = JSON.parse(e.data);
    const imgDataUrl = res.img;
    const frame_idx = res.frame_idx;

    $('#frame_idx').text(`Frame Number ${frame_idx}`);
    plotFig(imgDataUrl);
};