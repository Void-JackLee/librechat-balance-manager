#!/bin/sh

# 启动后端 API (绑定到 0.0.0.0)
echo "Starting API..."
npm run api &

# 启动前端 Dev (绑定到 0.0.0.0，否则外部无法访问)
echo "Starting Frontend..."
npm run dev -- --host 0.0.0.0 &

# 等待任一后台进程退出
wait -n

# 退出脚本
exit $?