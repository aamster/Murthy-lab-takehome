class VideoStreamer {
    constructor() {
        this.eventSource = null;
    }

    start() {
        const video = $('#videoSelect').val();
        this.eventSource = new EventSource(`/generate_predictions?video_name=${video}`);
        this.eventSource.onmessage = async e => {
            const res = JSON.parse(e.data);
            const imgDataUrl = res.img;
            const peakPoints = res.peak_points;
            const frame_idx = res.frame_idx;

            $('#frame_idx').text(`Frame Number ${frame_idx}`);
            this.plotFig(imgDataUrl, peakPoints);
        };

        this.eventSource.onerror = () => {
            $('#errorMsg').show();
            $('#startBtn').prop('disabled', false);
            this.eventSource.close();
        }

        this.eventSource.addEventListener('done', () => {
            $('#startBtn').prop('disabled', false);
            this.eventSource.close();
        });
    }

    plotFig(imgUrl, peakPoints) {
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
    }
}