<script lang="ts">
    import { type IconDefinition } from '@fortawesome/fontawesome-svg-core';

    export let icon: IconDefinition;
    export let color: string = '#ffffff';
    
    let width: number = icon.icon[0];
    let height: number = icon.icon[1];
    let path: string = icon.icon[4] as string;
</script>

<svg 
    xmlns='http://www.w3.org/2000/svg'
    aria-hidden="true"
    focusable="false"
    role="img"
    viewBox='0 0 {width} {height}'
>
    <path 
        d={path}
        fill={color}
    />
</svg>

<style>
    svg{
        width: 18px;
        height: 18px;
    }

    svg:hover {
        cursor: pointer;
    }
</style>