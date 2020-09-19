const evtSource = new EventSource('/generate_predictions?video_name=test_clip.15s.mp4');

const plotFig = (img, pred) => {
    img.forEach((row, i) => {
        img[i].forEach((col, ii) => {
            const v = img[i][ii];
            img[i][ii] = [v, v, v];
        });
    });
    
    const trace1 = {
        z: img,
        type: 'image'
    };

    const trace2 = {
        z: pred,
        type: 'heatmap',
        opacity: 0.5
    };

    const layout = {
        width: 800,
        height: 800
    };

    const plotExists = $('#plot.js-plotly-plot').length > 0;

    if(plotExists) {
        Plotly.restyle('plot', {z: [trace1.z, trace2.z]});
    } else {
        Plotly.newPlot('plot', [trace1, trace2], layout);
    }


};

let frame_idx = 0;

evtSource.onmessage = e => {
    const res = JSON.parse(e.data);
    let img = res.img;
    const pred = res.pred;
    const frame_idx = res.frame_idx;

    $('#frame_idx').text(`Frame Number ${frame_idx}`);
    plotFig(img, pred);
};