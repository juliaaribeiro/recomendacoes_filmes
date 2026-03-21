// DOM event types are available globally in TypeScript (lib.dom), so no import is needed.

export const setTargetStyle = (event: MouseEvent | FocusEvent, styles: Partial<CSSStyleDeclaration>) => {
  const target = (event.target || event.currentTarget) as HTMLElement | null
  if (!target) return
  Object.assign(target.style, styles)
}

export const setCurrentTargetStyle = (event: MouseEvent, styles: Partial<CSSStyleDeclaration>) => {
  const target = event.currentTarget as HTMLElement | null
  if (!target) return
  Object.assign(target.style, styles)
}
