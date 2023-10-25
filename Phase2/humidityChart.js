<script>
function drawHum(){
    // humidity
    var humidityChartDiv = am5.Root.new("humidityChart");

    humidityChartDiv.setThemes([
    am5themes_Animated.new(humidityChartDiv)
    ]);

    var chart = humidityChartDiv.container.children.push(am5radar.RadarChart.new(humidityChartDiv, {
    panX: false,
    panY: false,
    startAngle: 180,
    endAngle: 360
    }));

    var axisRenderer = am5radar.AxisRendererCircular.new(humidityChartDiv, {
    innerRadius: -10,
    strokeOpacity: 0.1
    });

    var xAxis = chart.xAxes.push(am5xy.ValueAxis.new(humidityChartDiv, {
    maxDeviation: 0,
    min: 0,
    max: 100,
    strictMinMax: true,
    renderer: axisRenderer
    }));

    var axisDataItem = xAxis.makeDataItem({});
    axisDataItem.set("value", 0);

    var bullet = axisDataItem.set("bullet", am5xy.AxisBullet.new(humidityChartDiv, {
    sprite: am5radar.ClockHand.new(humidityChartDiv, {
        radius: am5.percent(99)
    })
    }));

    xAxis.createAxisRange(axisDataItem);

    axisDataItem.get("grid").set("visible", false);

    setInterval(function () {
    axisDataItem.animate({
        key: "value",
        to: 40,
        easing: am5.ease.out(am5.ease.cubic)
    });
    }, 2000);


    // Make stuff animate on load
    chart.appear(1000, 100);
}

drawHum();

console.log("adsadfasasssssss");
console.log(aa);

</script>