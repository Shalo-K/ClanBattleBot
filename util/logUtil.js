const log4js = require('log4js');
log4js.configure('./conf/log4js_config.json');

module.exports = class logUtil{
    // ログ書込み
    writeLog(target, level, discription){
        const logger = log4js.getLogger(target);
        switch(level){
            case 'debug':
                logger.debug(discription);
                break;
            
            case 'info':
                logger.info(discription);
                break;
            
            case 'warn':
                logger.warn(discription);
                break;

            case 'error':
                logger.error(discription);

        }
    }    
}
