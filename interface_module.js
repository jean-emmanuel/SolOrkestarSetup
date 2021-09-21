HOST = '127.0.0.1'
PORT = 8080
SL_PORT = 9951
SL_SYNC = -1
SL_LENGTH = 1
SL_TIME = 0

module.exports = {

  init: ()=>{

    send(HOST, SL_PORT, `/sl/-1/unregister_auto_update`, 'loop_len', `osc.udp://${HOST}:${PORT}`, '/sl_time')
    send(HOST, SL_PORT, `/sl/-1/unregister_auto_update`, 'loop_post', `osc.udp://${HOST}:${PORT}`, '/sl_time')

    setInterval(()=>{

      send(HOST, SL_PORT, '/get', 'sync_source', `osc.udp://${HOST}:${PORT}`, '/sl_sync_change')

    }, 1000)


  },

  oscInFilter: (data)=>{

    var {host, port, address, args} = data

    if (address === '/sl_sync_change') {

      var sync = args[2].value
      if (SL_SYNC !== sync) {
        if (SL_SYNC !== -1) {
          send(HOST, SL_PORT, `/sl/${SL_SYNC - 1}/unregister_auto_update`, 'loop_len', `osc.udp://${HOST}:${PORT}`, '/sl_length')
          send(HOST, SL_PORT, `/sl/${SL_SYNC - 1}/unregister_auto_update`, 'loop_post', `osc.udp://${HOST}:${PORT}`, '/sl_time')
        }
        SL_SYNC = sync
        send(HOST, SL_PORT, `/sl/${SL_SYNC - 1}/get`, 'loop_len', `osc.udp://${HOST}:${PORT}`, '/sl_time')
        send(HOST, SL_PORT, `/sl/${SL_SYNC - 1}/get`, 'loop_pos', `osc.udp://${HOST}:${PORT}`, '/sl_time')
        send(HOST, SL_PORT, `/sl/${SL_SYNC - 1}/register_auto_update`, 'loop_len', 100, `osc.udp://${HOST}:${PORT}`, '/sl_length')
        send(HOST, SL_PORT, `/sl/${SL_SYNC - 1}/register_auto_update`, 'loop_pos', 100, `osc.udp://${HOST}:${PORT}`, '/sl_time')
      }

    }

    else if (address === '/sl_time') {

      SL_TIME = args[2].value

      receive('/sl_sync_position', SL_TIME / SL_LENGTH)

    }

    else if (address === '/sl_length') {

      SL_LENGTH = args[2].value

    }

    return data

  }

}
