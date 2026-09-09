package EnumTest;

/**
 * 订单状态枚举类
 * 
 * 枚举（enum）知识点：
 * 
 * 1. 枚举的本质：
 *    枚举是一种特殊的类，每个枚举项都是该类的「单例对象」
 *    编译后，枚举类会继承 java.lang.Enum 类
 * 
 * 2. 枚举 vs 常量：
 *    // 传统方式：用常量，不安全
 *    public static final int PAYMENT_PENDING = 0; // 可以传入任意 int
 *    
 *    // 枚举方式：类型安全，只能传入定义的枚举值
 *    public void updateState(OrderState state) { }
 * 
 * 3. 枚举的特点：
 *    - 构造方法默认且必须是 private（不能外部创建对象）
 *    - 所有枚举项默认用 public static final 修饰
 *    - 枚举项之间用逗号分隔，最后一个用分号
 *    - 枚举项必须在第一行定义
 * 
 * 4. 常用方法：
 *    - values()    : 获取所有枚举项（数组）
 *    - valueOf()   : 根据名称获取枚举项
 *    - ordinal()   : 获取枚举项的序号（从 0 开始）
 *    - name()      : 获取枚举项的名称（大写英文）
 *    - compareTo() : 比较两个枚举项的先后顺序
 */
public enum OrderState {

    // ==================== 枚举项定义 ====================
    // 格式：枚举项名(中文描述, 状态码)
    // 注意：枚举项必须在所有代码的最前面
    PAYMENT_PENDING("待支付", 0),
    PROCESSING("处理中", 1),
    SHIPPED("已发货", 2),
    OUT_FOR_DELIVERY("配送中", 3),
    DELIVERED("已送达", 4),
    CANCELLED("已取消", 5);

    // ==================== 成员变量 ====================
    private String name;  // 状态的中文描述
    private int code;     // 状态码（用于数据库存储）

    // ==================== 构造方法 ====================
    /**
     * 枚举的构造方法
     * 注意：枚举的构造方法默认是 private，不能省略 private 关键字
     * 每个枚举项在类加载时就会调用这个构造方法创建对象
     * 
     * @param name 状态的中文描述
     * @param code 状态码
     */
    private OrderState(String name, int code) {
        this.name = name;
        this.code = code;
    }

    // ==================== Getter 方法 ====================
    public String getName() {
        return name;
    }

    public int getCode() {
        return code;
    }

    // ==================== 工具方法 ====================
    /**
     * 根据状态码获取对应的枚举项
     * 常用于从数据库读取状态码后，转换为枚举对象
     * 
     * @param code 状态码
     * @return 对应的枚举项，找不到返回 null
     */
    public static OrderState getByCode(int code) {
        for (OrderState state : values()) {
            if (state.getCode() == code) {
                return state;
            }
        }
        return null;  // 找不到则返回 null
    }

    /**
     * 判断当前订单是否可以取消
     * 规则：只有"待支付"和"处理中"的订单可以取消
     * 
     * @return true=可以取消，false=不能取消
     */
    public boolean canCancel() {
        return this == PAYMENT_PENDING || this == PROCESSING;
    }

    /**
     * 判断订单是否已完成（不可逆状态）
     * 
     * @return true=已完成，false=未完成
     */
    public boolean isFinished() {
        return this == DELIVERED || this == CANCELLED;
    }

    /**
     * 重写 toString，方便打印
     * 输出格式：枚举名(中文描述, 状态码)
     */
    @Override
    public String toString() {
        return this.name() + "(" + this.name + ", " + this.code + ")";
    }
}