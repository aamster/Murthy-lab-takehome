const evtSource = new EventSource('/generate_predictions?video_name=test_clip.15s.mp4');

const plotFig = (imgUrl, peakPoints) => {
    const trace1 = {
        source: imgUrl,
        type: 'image'
    };

    const trace2 = {
        mode: 'markers',
        type: 'scatter',
        x: peakPoints.map(v => v[0]),
        y: peakPoints.map(v => v[1]),
        marker: {
            symbol: 'cross'
        }
    };

    const layout = {
        width: 1024,
        height: 1024
    };

    const plotExists = $('#plot.js-plotly-plot').length > 0;

    if(plotExists) {
        Plotly.restyle('plot', {source: [trace1.source]}, [0]);
        Plotly.restyle('plot', {x: [trace2.x], y: [trace2.y]}, [1]);
    } else {
        Plotly.newPlot('plot', [trace1, trace2], layout);
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
    const peakPoints = res.peak_points;
    const frame_idx = res.frame_idx;

    $('#frame_idx').text(`Frame Number ${frame_idx}`);
    plotFig(imgDataUrl, peakPoints);
};