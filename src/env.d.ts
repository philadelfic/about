/// <reference types="astro/client" />

declare namespace astroHTML.JSX {
  interface SVGAttributes {
    /**
     * Атрибут hidden у SVG-иконок (солнце/луна в BaseLayout): в типах Astro его
     * у SVG-элементов нет, а в разметке он нужен до первого переключения темы.
     */
    hidden?: boolean | 'until-found';
  }
}
