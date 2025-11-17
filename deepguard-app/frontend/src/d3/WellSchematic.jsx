import React, { useEffect, useRef } from 'react'
import * as d3 from 'd3'

export default function WellSchematic({ schematic }) {
  const ref = useRef()

  useEffect(() => {
    if (!schematic || !schematic.depths) return
    const svg = d3.select(ref.current)
    svg.selectAll('*').remove()

    const width = 300
    const height = 500
    svg.attr('viewBox', `0 0 ${width} ${height}`)

    const scale = d3.scaleLinear().domain([0, schematic.depths]).range([50, height - 20])

    // depth axis
    const axis = d3.axisLeft(scale).ticks(5)
    svg.append('g').attr('transform', 'translate(40,0)').call(axis)

    // casings
    schematic.casings.forEach((casing, i) => {
      svg
        .append('rect')
        .attr('x', 80 + i * 10)
        .attr('y', scale(casing.top_md))
        .attr('width', 40 - i * 10)
        .attr('height', scale(casing.bottom_md) - scale(casing.top_md))
        .attr('fill', '#94a3b8')
        .attr('opacity', 0.6)
    })

    // tubing
    schematic.tubing.forEach(tube => {
      svg
        .append('rect')
        .attr('x', 130)
        .attr('y', scale(tube.top_md))
        .attr('width', 20)
        .attr('height', scale(tube.bottom_md) - scale(tube.top_md))
        .attr('fill', '#0ea5e9')
    })

    // barrier elements
    schematic.barrier_elements.forEach(barrier => {
      svg
        .append('circle')
        .attr('cx', 140)
        .attr('cy', scale(barrier.md))
        .attr('r', 6)
        .attr('fill', barrier.status === 'tested' ? '#22c55e' : '#f97316')
        .append('title')
        .text(`${barrier.name} (${barrier.type})`)
    })

    // annulus status bars
    schematic.annuli.forEach((annulus, idx) => {
      const statusColor = {
        'GREEN': '#22c55e',
        'AMBER': '#f59e0b',
        'HIGH-AMBER': '#fb923c',
        'RED': '#ef4444',
      }[annulus.status] || '#cbd5e1'
      svg
        .append('rect')
        .attr('x', 200)
        .attr('y', 60 + idx * 40)
        .attr('width', 80)
        .attr('height', 20)
        .attr('fill', statusColor)
      svg
        .append('text')
        .attr('x', 240)
        .attr('y', 75 + idx * 40)
        .attr('text-anchor', 'middle')
        .attr('fill', '#0f172a')
        .text(`${annulus.name}: ${(annulus.utilisation * 100).toFixed(1)}%`)
    })
  }, [schematic])

  return <svg ref={ref} className="w-full h-[500px] bg-white rounded shadow"></svg>
}
