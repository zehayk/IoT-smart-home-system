//<script>
function drawTemp() {
    console.log("LALALALALA");
    // temperature

    var temperatureChartDiv = am5.Root.new("tempChart");

    // Set themes
    // https://www.amcharts.com/docs/v5/concepts/themes/
    temperatureChartDiv.setThemes([
    am5themes_Animated.new(temperatureChartDiv)
    ]);

    // Create chart
    // https://www.amcharts.com/docs/v5/charts/radar-chart/
    var chartTemp = temperatureChartDiv.container.children.push(am5radar.RadarChart.new(temperatureChartDiv, {
    panX: false,
    panY: false,
    startAngle: 180,
    endAngle: 360
    }));


    // Create axis and its renderer
    // https://www.amcharts.com/docs/v5/charts/radar-chart/gauge-charts/#Axes
    var axisRenderer = am5radar.AxisRendererCircular.new(temperatureChartDiv, {
    innerRadius: -10,
    strokeOpacity: 0.1
    });

    var xAxis = chartTemp.xAxes.push(am5xy.ValueAxis.new(temperatureChartDiv, {
    maxDeviation: 0,
    min: 0,
    max: 100,
    strictMinMax: true,
    renderer: axisRenderer
    }));


    // Add clock hand
    // https://www.amcharts.com/docs/v5/charts/radar-chart/gauge-charts/#Clock_hands
    var axisDataItem = xAxis.makeDataItem({});
    axisDataItem.set("value", 0);

    var bullet = axisDataItem.set("bullet", am5xy.AxisBullet.new(temperatureChartDiv, {
    sprite: am5radar.ClockHand.new(temperatureChartDiv, {
        radius: am5.percent(99)
    })
    }));

    xAxis.createAxisRange(axisDataItem);

    axisDataItem.get("grid").set("visible", false);

    setInterval(function () {
    // axisDataItem.animate({
    //     key: "value",
    //     to: Math.round(Math.random() * 100),
    //     duration: 800,
    //     easing: am5.ease.out(am5.ease.cubic)
    // });
    axisDataItem.animate({
        key: "value",
        to: 40,
        easing: am5.ease.out(am5.ease.cubic)
    });
    }, 2000);


    // Make stuff animate on load
    chartTemp.appear(1000, 100);
}

drawTemp();
console.log("FUCK YOU ITS 12AM I WANNA SLEEP");
//</script>
//<div id="tempChart" style="width: 50vw;height: 300px" onload="drawTemp()"></div>