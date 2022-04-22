import One from './page/one';
import Two from './page/two';

const routes = [
    { path: '/', component: One, exact : true },
    { path: '/two', component: Two,},
  ];
  
  export default routes;