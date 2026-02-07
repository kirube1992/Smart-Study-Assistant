'use client'
import React from 'react';
export function Select(props:any){ return <select {...props} />; }
export function SelectContent({children}:{children:any}){ return <div>{children}</div>; }
export function SelectItem({children,value}:{children:any,value?:string}){ return <div data-value={value}>{children}</div>; }
export function SelectTrigger(props:any){ return <div {...props}/>; }
export function SelectValue(props:any){ return <span {...props}/>; }
