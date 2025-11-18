import { useEffect, useRef } from 'react'
import * as d3 from 'd3'

export default function WellSchematic({ data }) {
  const ref = useRef(null)

  useEffect(() => {
    if (!data) return
    const svg = d3.select(ref.current)
    svg.selectAll('*').remove()
    const width = 420
    const height = 600
    const margin = { top: 20, right: 80, bottom: 20, left: 80 }

    const depthScale = d3.scaleLinear().domain([0, 2600]).range([margin.top, height - margin.bottom])

    // casing strings
    svg
      .selectAll('rect.casing')
      .data(data.casing_strings)
      .enter()
      .append('rect')
      .attr('class', 'casing')
      .attr('x', width / 2 - 60)
      .attr('width', 120)
      .attr('y', d => depthScale(d.top))
      .attr('height', d => depthScale(d.bottom) - depthScale(d.top))
      .attr('fill', '#1E2538')
      .attr('stroke', '#4B5563')
      .attr('stroke-width', 2)
      .attr('opacity', 0.85)

    // tubing
    svg
      .selectAll('rect.tubing')
      .data(data.tubing)
      .enter()
      .append('rect')
      .attr('x', width / 2 - 15)
      .attr('width', 30)
      .attr('y', d => depthScale(d.top))
      .attr('height', d => depthScale(d.bottom) - depthScale(d.top))
      .attr('fill', 'url(#tubingGradient)')

    // gradient for tubing
    const defs = svg.append('defs')
    const gradient = defs.append('linearGradient').attr('id', 'tubingGradient').attr('x1', '0%').attr('x2', '0%').attr('y1', '0%').attr('y2', '100%')
    gradient.append('stop').attr('offset', '0%').attr('stop-color', '#1CD9A1')
    gradient.append('stop').attr('offset', '100%').attr('stop-color', '#0EA371')

    // barrier elements
    svg
      .selectAll('circle.barrier')
      .data(data.barrier_elements)
      .enter()
      .append('circle')
      .attr('cx', width / 2)
      .attr('cy', d => depthScale(d.depth))
      .attr('r', 10)
      .attr('fill', d => d.status === 'OK' ? '#1CD9A1' : '#FF5A63')
      .append('title')
      .text(d => `${d.type} - ${d.name}`)

    const axis = d3.axisLeft(depthScale).ticks(8).tickFormat(d => `${d} m`)
    svg.append('g').attr('transform', `translate(${margin.left},0)`).call(axis).selectAll('text').style('fill', '#9CA3AF')
  }, [data])

  return <svg ref={ref} viewBox="0 0 420 600" className="w-full h-[600px]" />
}
