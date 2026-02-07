'use client'
import {useCallback} from 'react';
export function useToast(){
  const toast = useCallback((opts:{title?:string,description?:string,variant?:string})=>{
    const title = opts && opts.title ? opts.title + ': ' : '';
    const description = opts && opts.description ? opts.description : '';
    const msg = title + description;
    alert(msg);
  },[]);
  return { toast };
}
