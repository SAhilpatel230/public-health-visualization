// script.js
document.addEventListener('DOMContentLoaded', function () {
    const filterForm = document.getElementById('filter-form');
    const metricSelect = document.getElementById('metric-select');
    const stateSelect = document.getElementById('state');
    const countySelect = document.getElementById('county');
    const minValueInput = document.getElementById('min_value');
    const maxValueInput = document.getElementById('max_value');
    const sortSelect = document.getElementById('sort-select');
    const xAxisSelect = document.getElementById('x-axis');
    const yAxisSelect = document.getElementById('y-axis');
    const chartTypeSelect = document.getElementById('chart-type');

    const metricOptions = {
        'life_expectancy': {
            x: ['state', 'county', 'census_tract'],
            y: ['life_expectancy', 'standard_error']
        },
        'immunization_coverage': {
            x: ['geography', 'birth_year', 'vaccine'],
            y: ['estimate', 'dose']
        },
        'mortality_rate': {
            x: ['state', 'year', 'cause'],
            y: ['deaths', 'age_adjusted_rate']
        }
    };

    function updateAxes() {
        const metric = metricSelect.value;
        const options = metricOptions[metric];

        xAxisSelect.innerHTML = '';
        yAxisSelect.innerHTML = '';

        options.x.forEach(option => {
            const opt = document.createElement('option');
            opt.value = option;
            opt.textContent = option.replace('_', ' ').toUpperCase();
            xAxisSelect.appendChild(opt);
        });

        options.y.forEach(option => {
            const opt = document.createElement('option');
            opt.value = option;
            opt.textContent = option.replace('_', ' ').toUpperCase();
            yAxisSelect.appendChild(opt);
        });
    }

    metricSelect.addEventListener('change', function () {
        updateAxes();
        filterForm.submit();
    });

    chartTypeSelect.addEventListener('change', updateChart);

    // Chart.js setup
    const ctx = document.getElementById('metric-chart').getContext('2d');
    let metricChart = new Chart(ctx, {
        type: chartTypeSelect.value,
        data: {
            labels: [],
            datasets: [{
                label: 'Metric Data',
                data: [],
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: xAxisSelect.value
                    }
                },
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: yAxisSelect.value
                    }
                }
            }
        }
    });

    function updateChart() {
        fetch(`/api/chart-data?metric=${metricSelect.value}&x_axis=${xAxisSelect.value}&y_axis=${yAxisSelect.value}`)
            .then(response => response.json())
            .then(data => {
                metricChart.destroy();
                metricChart = new Chart(ctx, {
                    type: chartTypeSelect.value,
                    data: {
                        labels: data.labels,
                        datasets: [{
                            label: 'Metric Data',
                            data: data.values,
                            backgroundColor: 'rgba(75, 192, 192, 0.2)',
                            borderColor: 'rgba(75, 192, 192, 1)',
                            borderWidth: 1
                        }]
                    },
                    options: {
                        responsive: true,
                        scales: {
                            x: {
                                beginAtZero: true,
                                title: {
                                    display: true,
                                    text: xAxisSelect.value
                                }
                            },
                            y: {
                                beginAtZero: true,
                                title: {
                                    display: true,
                                    text: yAxisSelect.value
                                }
                            }
                        }
                    }
                });
            });
    }

    [metricSelect, xAxisSelect, yAxisSelect, chartTypeSelect].forEach(element => {
        element.addEventListener('change', updateChart);
    });

    updateAxes();
    updateChart();
});