// eslint-disable-next-line no-undef
importScripts('./jszip.min.js');

// Worker 线程
self.onmessage = function (e) {
  var url = e.data;
  // console.log('url', url);
  // console.log(this);

  var xhr = new XMLHttpRequest();
  xhr.open('GET', url, true);
  xhr.responseType = 'arraybuffer';
  xhr.send();

  xhr.onload = () => {
    let bufferData = xhr.response;
    // console.log('dddd', bufferData); // Hello, world!
    JSZip.loadAsync(bufferData, { base64: true }).then(zip => {
      // console.log('zip', zip.files);
      zip.files['jrh.obj']
        .async('text')
        .then(text => {
          postMessage({ success: 1, data: text });
          this.close();
        })
        .catch(err => {
          postMessage({ success: 0, data: err });
          this.close();
        });
    });

    bufferData = null;
  };
  xhr.onerror = () => {
    let err = xhr.response;
    // console.log('eee', err); // Hello, world!
    postMessage({ success: 0, data: err });
    err = null;
    this.close();
  };

  // $.ajax({
  //   method: 'get',
  //   url,
  //   contentType: 'application/zip',
  //   xhrFields: { responseType: 'arraybuffer' } // 类型必须为arraybuffer
  // })
  //   .done(data => {
  //     console.log('file', data);
  //     postMessage({ success: 1, data: data });
  //     this.close();
  //   })
  //   .fail((err) => {
  //     postMessage({ success: 0, data: err });
  //     this.close();
  //   });

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
