declare module '@heroicons/react/outline' {
  import { FC, SVGProps } from 'react';
  
  export interface IconProps extends SVGProps<SVGSVGElement> {
    className?: string;
  }

  export const SearchIcon: FC<IconProps>;
  export const HomeIcon: FC<IconProps>;
  export const ChartBarIcon: FC<IconProps>;
  export const SparklesIcon: FC<IconProps>;
} 