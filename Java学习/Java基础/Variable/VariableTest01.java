package Variable;
// 模拟钱包
public class VariableTest01 {
    public static void main(String[] args) {
        /* 微信余额：0元
        支付宝余额：10元
        银行卡余额：20元
        问题一：请问现在一共多少钱
        问题二：微信收了10元，又发了2元红包，余额多少？ */
        // 创建一个 Wallet 对象
        Wallet wallet = new Wallet();

        // 初始化余额
        wallet.setWechat(0);
        wallet.setAlipay(10);
        wallet.setBank(20);

        // 调用 getTotal 方法输出总金额
        System.out.println("一共：" + wallet.getTotal() + "元");
        
        // 调用 wechatReceive 方法，微信收款 10 元
        wallet.wechatReceive(10);
        // 调用 wechatSend 方法，微信发红包 2 元
        wallet.wechatSend(2);

        // 调用 getTotal 方法输出总金额
        System.out.println("一共：" + wallet.getTotal() + "元");
    }
}


class Wallet {
    // 定义属性
    private double wechat;
    private double alipay;
    private double bank;
    
    // 获取总金额
    public double getTotal() {
        return wechat + alipay + bank;
    }
    
    // 微信收款
    public void wechatReceive(double amount) {
        wechat += amount;
    }
    
    // 微信发红包
    public void wechatSend(double amount) {
        wechat -= amount;
    }
    
    // getter 和 setter
    public double getWechat() {
        return wechat;
    }
    
    public void setWechat(double wechat) {
        this.wechat = wechat;
    }
    
    public double getAlipay() {
        return alipay;
    }
    
    public void setAlipay(double alipay) {
        this.alipay = alipay;
    }
    
    public double getBank() {
        return bank;
    }
    
    public void setBank(double bank) {
        this.bank = bank;
    }
}