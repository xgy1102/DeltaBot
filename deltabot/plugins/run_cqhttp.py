from nonebot import on_startup
from loguru import logger
import subprocess
import os
# import logging
# import threading

from .. import config


def config_cqhttp():
    with open('cqhttp/config_template.hjson', 'r') as f:
        cq_config = f.read()

    cq_config = cq_config.replace('[uin]', str(config.UIN))
    cq_config = cq_config.replace('[password]', str(config.PASSWORD))
    cq_config = cq_config.replace('[port]', str(config.PORT))

    with open('cqhttp/config.hjson', 'w') as f:
        f.write(cq_config)


@on_startup
async def run_cqhttp():
    # TODO 使用loguru处理go-cqhttp输出

    # def log_cqhttp(cqhttp_process):
    #     with cqhttp_process.stdout:
    #         for line in iter(cqhttp_process.stdout.readline, b''):  # b'\n'-separated lines
    #             logger.info(line.decode('utf-8').strip())

    config_cqhttp()

    # Check is go-cqhttp executable
    if not os.access('cqhttp/go-cqhttp', os.X_OK):
        mode = os.stat('cqhttp/go-cqhttp').st_mode | 0o100
        logger.warning("go-cqhttp is not executable! Sudo authority required to set permissions.")
        os.chmod('cqhttp/go-cqhttp', mode)
        logger.info("Set permissions successful. Sudo authority will not required on next running.")


    logger.info("Start go-cqhttp!")
    cqhttp_process = subprocess.Popen(['cd cqhttp;./go-cqhttp'], shell=True)


    #                                   stdout=subprocess.PIPE,
    #                                   stderr=subprocess.STDOUT)
    # cqhttp_log_thread = threading.Thread(target=log_cqhttp, args=[cqhttp_process])
    # cqhttp_log_thread.run()