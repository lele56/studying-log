package EnumTest;

/**
 * 测试类：演示枚举的完整用法
 * 
 * 枚举的核心优势：
 * 1. 类型安全：入参只能是枚举项，不会传入非法值
 * 2. 代码可读：ORDER_STATE.PAYMENT_PENDING 比 0 更直观
 * 3. 自带方法：values()、valueOf()、ordinal() 等
 * 4. 适合 switch：枚举天生适合 switch 语句
 */
public class test01 {
    public static void main(String[] args) {
        /*
         * 电商项目中，订单的状态只有以下 6 种，请编写代码实现。
         * 待支付    PAYMENT_PENDING    
         * 处理中    PROCESSING
         * 已发货    SHIPPED
         * 配送中    OUT_FOR_DELIVERY
         * 已送达    DELIVERED
         * 已取消    CANCELLED
         * 
         * javabean ---> 枚举
         * 定义 javabean 类，描述电商项目种订单的状态
         */

        // ==================== 1. 获取枚举对象 ====================
        System.out.println("==================== 1. 获取枚举对象 ====================");
        // 枚举项默认用 public static final 修饰，通过 类名.枚举项 直接访问
        OrderState orderState = OrderState.PAYMENT_PENDING;
        System.out.println("当前状态：" + orderState.getName());
        System.out.println("状态码：" + orderState.getCode());
        System.out.println("完整信息：" + orderState.toString());

        // ==================== 2. 遍历所有枚举项 ====================
        System.out.println("\n==================== 2. 遍历所有枚举项 ====================");
        // values() 返回所有枚举项的数组
        OrderState[] states = OrderState.values();
        for (OrderState state : states) {
            System.out.println("  " + state.ordinal() + " - " + state.getName() + " (状态码: " + state.getCode() + ")");
        }

        // ==================== 3. valueOf() 字符串转枚举 ====================
        System.out.println("\n==================== 3. valueOf() 字符串转枚举 ====================");
        // 通过枚举项名称（大写英文）获取枚举对象
        OrderState shipped = OrderState.valueOf("SHIPPED");
        System.out.println("SHIPPED 对应的中文：" + shipped.getName());

        // ==================== 4. getByCode() 状态码转枚举 ====================
        System.out.println("\n==================== 4. getByCode() 状态码转枚举 ====================");
        // 从数据库读取状态码 3，转换为枚举对象
        OrderState stateByCode = OrderState.getByCode(3);
        System.out.println("状态码 3 对应：" + stateByCode.getName());

        // ==================== 5. switch 中使用枚举 ====================
        System.out.println("\n==================== 5. switch 中使用枚举 ====================");
        OrderState currentState = OrderState.PROCESSING;
        switch (currentState) {
            case PAYMENT_PENDING:
                System.out.println("订单待支付，请尽快付款");
                break;
            case PROCESSING:
                System.out.println("订单处理中，请耐心等待");
                break;
            case SHIPPED:
                System.out.println("订单已发货，请注意查收");
                break;
            case OUT_FOR_DELIVERY:
                System.out.println("快递员正在配送中");
                break;
            case DELIVERED:
                System.out.println("订单已送达，请确认收货");
                break;
            case CANCELLED:
                System.out.println("订单已取消");
                break;
        }

        // ==================== 6. 枚举的业务方法 ====================
        System.out.println("\n==================== 6. 枚举的业务方法 ====================");
        // canCancel() 判断是否可以取消
        System.out.println("待支付可以取消吗？" + OrderState.PAYMENT_PENDING.canCancel());
        System.out.println("已发货可以取消吗？" + OrderState.SHIPPED.canCancel());

        // isFinished() 判断是否已完成
        System.out.println("已送达是终态吗？" + OrderState.DELIVERED.isFinished());
        System.out.println("配送中是终态吗？" + OrderState.OUT_FOR_DELIVERY.isFinished());

        // ==================== 7. 枚举比较 ====================
        System.out.println("\n==================== 7. 枚举比较 ====================");
        // 枚举可以直接用 == 比较（因为每个枚举项都是单例）
        OrderState state1 = OrderState.DELIVERED;
        OrderState state2 = OrderState.DELIVERED;
        System.out.println("state1 == state2 ? " + (state1 == state2));  // true

        // name() 获取枚举项的名称（大写英文）
        System.out.println("枚举项名称：" + OrderState.PROCESSING.name());  // PROCESSING

        // ordinal() 获取枚举项的序号（从 0 开始）
        System.out.println("配送中的序号：" + OrderState.OUT_FOR_DELIVERY.ordinal());  // 3
    }
}