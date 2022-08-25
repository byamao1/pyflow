// eslint-disable-next-line no-undef
importScripts('./three.min.js', './OBJLoader.js');

// Worker 线程
self.onmessage = function (e) {
  var url = e.data;
  console.log('url', url);
  postMessage({ success: 1, data: 'obj' });
  // const loader = new THREE.OBJLoader();
  // // ip:5000/3d/jrhb3sh9-25-c-01_asm.obj
  // // 加载OBJ
  // loader.load(
  //   url,
  //   obj => {
  //     console.log('object', obj);
  //     // 初始化模型坐标值（根据需要自行调整）
  //     obj.name = 'reducer';
  //     obj.position.set(0, 0, 0);
  //     postMessage({ success: 1, data: 'obj' });
  //   },
  //   function (xhr) {},
  //   function (error) {
  //     postMessage({ success: 0, data: 'obj' });
  //   }
  // );
};
