import { useEffect, useRef } from 'react'
import * as d3 from 'd3'

export default function WellSchematic({ schematic }) {
  const ref = useRef(null)

  useEffect(() => {
    const svg = d3.select(ref.current)
    svg.selectAll('*').remove()
    const width = 400, height = 600
    svg.attr('viewBox', `0 0 ${width} ${height}`)

    const scale = d3.scaleLinear().domain([0, schematic.well.tvd || 2000]).range([50, height-50])

    // casing representation
    const casings = [
      { width: 120, label: 'Conductor' },
      { width: 100, label: 'Surface' },
      { width: 70, label: 'Production' },
      { width: 40, label: 'Tubing' },
    ]

    casings.forEach((c, i) => {
      svg.append('rect')
        .attr('x', (width - c.width)/2)
        .attr('y', 40 + i*10)
        .attr('width', c.width)
        .attr('height', height-100)
        .attr('rx', 12)
        .attr('fill', `url(#grad${i})`)
        .attr('opacity', 0.1)
        .attr('stroke', '#7af0ff')
        .attr('stroke-width', 1)
    })

    svg.append('defs')
      .selectAll('linearGradient')
      .data(casings)
      .enter()
      .append('linearGradient')
      .attr('id', (_, i)=>`grad${i}`)
      .attr('x1','0%').attr('y1','0%').attr('x2','0%').attr('y2','100%')
      .each(function(){
        d3.select(this).append('stop').attr('offset','0%').attr('stop-color','#7af0ff').attr('stop-opacity',0.15)
        d3.select(this).append('stop').attr('offset','100%').attr('stop-color','#7af0ff').attr('stop-opacity',0.02)
      })

    schematic.barrier_elements?.forEach((b, idx) => {
      svg.append('circle')
        .attr('cx', width/2)
        .attr('cy', scale(b.depth || 0))
        .attr('r', 6)
        .attr('fill', b.status === 'FAILED' ? '#f87171' : '#7af0ff')
      svg.append('text')
        .attr('x', width/2 + 12)
        .attr('y', scale(b.depth || 0) + 4)
        .attr('fill', '#e2e8f0')
        .attr('font-size', 10)
        .text(`${b.barrier_type} ${b.name}`)
    })

    const pressure = schematic.annuli_pressures?.[0]
    if (pressure) {
      const statusColor = schematic.status === 'RED' ? '#ef4444' : schematic.status === 'HIGH-AMBER' ? '#fb923c' : schematic.status === 'AMBER' ? '#facc15' : '#22c55e'
      svg.append('rect')
        .attr('x', width - 130)
        .attr('y', 60)
        .attr('width', 110)
        .attr('height', 40)
        .attr('rx', 8)
        .attr('fill', statusColor)
        .attr('opacity', 0.2)
      svg.append('text').attr('x', width-120).attr('y', 85).attr('fill', '#e2e8f0').text(`P: ${pressure.pressure_bar} bar`)
    }
  }, [schematic])

  return <svg ref={ref} className="w-full h-[600px]" />
}
