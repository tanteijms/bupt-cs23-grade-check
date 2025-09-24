// 学生数据存储
let studentsData = {};

// 背景图片配置
const backgroundConfig = {
    images: [
        { file: './images/bocchi.jpg', name: '后藤一里', color: '#FFB6C1' },
        { file: './images/kita.jpg', name: '喜多郁代', color: '#98FB98' },
        { file: './images/ryo.jpg', name: '山田凉', color: '#87CEEB' },
        { file: './images/nijika.jpg', name: '伊地知虹夏', color: '#F0E68C' }
    ],
    current: null,
    isLoading: false
};

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    loadData();
    initializeEventListeners();
    initializeBackground();
    preloadBackgroundImages();
});

// 加载学生数据
async function loadData() {
    try {
        const response = await fetch('data.json');
        if (!response.ok) {
            throw new Error('数据加载失败');
        }
        studentsData = await response.json();
        console.log('数据加载成功，共', Object.keys(studentsData).length, '名学生');
    } catch (error) {
        console.error('数据加载错误:', error);
        showError('数据加载失败，请刷新页面重试');
    }
}

// 初始化事件监听器
function initializeEventListeners() {
    const studentIdInput = document.getElementById('studentId');
    const searchBtn = document.getElementById('searchBtn');

    // 输入框回车键搜索
    studentIdInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            searchGrade();
        }
    });

    // 输入框实时验证
    studentIdInput.addEventListener('input', function(e) {
        const value = e.target.value;
        // 只允许数字输入
        e.target.value = value.replace(/[^0-9]/g, '');
        
        // 更新搜索按钮状态
        updateSearchButtonState();
    });

    // 搜索按钮点击
    searchBtn.addEventListener('click', searchGrade);

    // 背景控制按钮
    const changeBgBtn = document.getElementById('changeBgBtn');
    const bgInfoBtn = document.getElementById('bgInfoBtn');
    
    if (changeBgBtn) {
        changeBgBtn.addEventListener('click', changeBackground);
    }
    
    if (bgInfoBtn) {
        bgInfoBtn.addEventListener('click', showBackgroundInfo);
    }
}

// 更新搜索按钮状态
function updateSearchButtonState() {
    const studentId = document.getElementById('studentId').value.trim();
    const searchBtn = document.getElementById('searchBtn');
    
    if (studentId.length >= 8) {
        searchBtn.classList.add('active');
    } else {
        searchBtn.classList.remove('active');
    }
}

// 搜索成绩主函数
async function searchGrade() {
    const studentId = document.getElementById('studentId').value.trim();
    
    // 验证输入
    if (!validateInput(studentId)) {
        return;
    }

    // 显示加载状态
    showLoading(true);

    try {
        // 模拟网络延迟，提升用户体验
        await new Promise(resolve => setTimeout(resolve, 300));

        // 查找学生数据
        const studentData = studentsData[studentId];
        
        if (studentData) {
            displayResult(studentData);
            showResultSection(true);
        } else {
            showError('未找到该学号的成绩记录，请检查学号是否正确');
            showResultSection(false);
        }
    } catch (error) {
        console.error('查询错误:', error);
        showError('查询过程中发生错误，请重试');
        showResultSection(false);
    } finally {
        showLoading(false);
    }
}

// 验证输入
function validateInput(studentId) {
    if (!studentId) {
        showError('请输入学号');
        return false;
    }

    if (studentId.length < 8) {
        showError('学号长度不正确，请输入完整的学号');
        return false;
    }

    if (!/^\d+$/.test(studentId)) {
        showError('学号格式不正确，只能包含数字');
        return false;
    }

    return true;
}

// 显示查询结果
function displayResult(studentData) {
    const resultContent = document.getElementById('resultContent');
    
    // 确定学生类型样式
    const studentTypeClass = studentData.学生类型 === '转入' ? 'transfer' : 'regular';
    const studentTypeIcon = studentData.学生类型 === '转入' ? 'fa-user-plus' : 'fa-user-check';
    
    // 构建结果HTML
    resultContent.innerHTML = `
        <div class="student-card">
            <div class="student-header">
                <div class="student-id">
                    <i class="fas fa-id-card"></i>
                    <span>学号: ${studentData.学号}</span>
                </div>
                <div class="student-type ${studentTypeClass}">
                    <i class="fas ${studentTypeIcon}"></i>
                    <span>${studentData.学生类型}学生</span>
                </div>
            </div>
            
            <div class="rank-display">
                <div class="rank-number">${studentData.排名}</div>
                <div class="rank-label">班级排名</div>
                <div class="rank-total">/ 358人</div>
            </div>
            
            <div class="grades-container">
                <div class="grade-item weighted">
                    <div class="grade-icon">
                        <i class="fas fa-star"></i>
                    </div>
                    <div class="grade-content">
                        <div class="grade-value">${studentData.加权平均分}</div>
                        <div class="grade-label">加权平均分</div>
                    </div>
                </div>
                
                ${studentData.大一成绩 !== null ? `
                <div class="grade-item">
                    <div class="grade-icon">
                        <i class="fas fa-graduation-cap"></i>
                    </div>
                    <div class="grade-content">
                        <div class="grade-value">${studentData.大一成绩}</div>
                        <div class="grade-label">大一成绩</div>
                    </div>
                </div>
                ` : ''}
                
                <div class="grade-item">
                    <div class="grade-icon">
                        <i class="fas fa-book"></i>
                    </div>
                    <div class="grade-content">
                        <div class="grade-value">${studentData.大二成绩}</div>
                        <div class="grade-label">大二成绩</div>
                    </div>
                </div>
            </div>
            
            ${studentData.学生类型 === '转入' ? `
            <div class="transfer-note">
                <i class="fas fa-info-circle"></i>
                <span>该学生为转入学生，只有大二成绩参与排名计算</span>
            </div>
            ` : ''}
            
            <div class="result-actions">
                <button class="share-btn" onclick="shareResult('${studentData.学号}')">
                    <i class="fas fa-share-alt"></i>
                    <span>分享结果</span>
                </button>
                <button class="print-btn" onclick="printResult()">
                    <i class="fas fa-print"></i>
                    <span>打印结果</span>
                </button>
            </div>
        </div>
    `;

    // 添加动画效果
    requestAnimationFrame(() => {
        resultContent.classList.add('show');
    });
}

// 显示/隐藏结果区域
function showResultSection(show) {
    const resultSection = document.getElementById('resultSection');
    const resultContent = document.getElementById('resultContent');
    
    if (show) {
        resultSection.style.display = 'block';
        // 平滑滚动到结果区域
        setTimeout(() => {
            resultSection.scrollIntoView({ 
                behavior: 'smooth', 
                block: 'nearest' 
            });
        }, 100);
    } else {
        resultSection.style.display = 'none';
        resultContent.classList.remove('show');
    }
}

// 清除结果
function clearResult() {
    showResultSection(false);
    document.getElementById('studentId').value = '';
    document.getElementById('studentId').focus();
    updateSearchButtonState();
}

// 显示/隐藏加载状态
function showLoading(show) {
    const loading = document.getElementById('loading');
    const searchBtn = document.getElementById('searchBtn');
    
    if (show) {
        loading.style.display = 'flex';
        searchBtn.disabled = true;
        searchBtn.classList.add('loading');
    } else {
        loading.style.display = 'none';
        searchBtn.disabled = false;
        searchBtn.classList.remove('loading');
    }
}

// 显示错误信息
function showError(message) {
    // 创建错误提示元素
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-toast';
    errorDiv.innerHTML = `
        <i class="fas fa-exclamation-triangle"></i>
        <span>${message}</span>
    `;
    
    document.body.appendChild(errorDiv);
    
    // 显示动画
    requestAnimationFrame(() => {
        errorDiv.classList.add('show');
    });
    
    // 3秒后自动隐藏
    setTimeout(() => {
        errorDiv.classList.remove('show');
        setTimeout(() => {
            if (errorDiv.parentNode) {
                errorDiv.parentNode.removeChild(errorDiv);
            }
        }, 300);
    }, 3000);
}

// 分享结果功能
function shareResult(studentId) {
    const student = studentsData[studentId];
    if (!student) return;
    
    const shareText = `我在北邮计算机学院2023级智育成绩查询系统中查到了我的成绩：
班级排名: ${student.排名}/358
加权平均分: ${student.加权平均分}
学生类型: ${student.学生类型}学生`;

    if (navigator.share) {
        navigator.share({
            title: '北邮计算机学院2023级智育成绩',
            text: shareText,
            url: window.location.href
        });
    } else if (navigator.clipboard) {
        navigator.clipboard.writeText(shareText).then(() => {
            showSuccess('成绩信息已复制到剪贴板');
        });
    } else {
        // 降级处理
        const textarea = document.createElement('textarea');
        textarea.value = shareText;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        showSuccess('成绩信息已复制到剪贴板');
    }
}

// ============================
// 背景相关功能
// ============================

// 初始化背景
function initializeBackground() {
    // 尝试从本地存储获取上次选择的背景
    const savedBackground = localStorage.getItem('preferredBackground');
    
    if (savedBackground) {
        const backgroundIndex = backgroundConfig.images.findIndex(bg => bg.file === savedBackground);
        if (backgroundIndex !== -1) {
            setBackground(backgroundIndex);
            return;
        }
    }
    
    // 如果没有保存的背景或找不到，则随机选择
    setRandomBackground();
}

// 设置随机背景
function setRandomBackground() {
    const randomIndex = Math.floor(Math.random() * backgroundConfig.images.length);
    setBackground(randomIndex);
}

// 设置指定背景
function setBackground(index, showLoading = false) {
    if (backgroundConfig.isLoading) return;
    
    const background = backgroundConfig.images[index];
    if (!background) return;
    
    if (showLoading) {
        showBackgroundLoading(true);
    }
    
    backgroundConfig.isLoading = true;
    
    // 预加载图片
    const img = new Image();
    img.onload = function() {
        // 设置背景
        document.body.style.backgroundImage = `url('${background.file}')`;
        document.body.style.backgroundSize = 'cover';
        document.body.style.backgroundPosition = 'center';
        document.body.style.backgroundAttachment = 'fixed';
        document.body.style.backgroundRepeat = 'no-repeat';
        
        // 更新当前背景信息
        backgroundConfig.current = background;
        updateBackgroundInfo();
        
        // 保存到本地存储
        localStorage.setItem('preferredBackground', background.file);
        
        backgroundConfig.isLoading = false;
        
        if (showLoading) {
            showBackgroundLoading(false);
        }
        
        // 添加切换动画效果
        document.body.classList.add('background-changed');
        setTimeout(() => {
            document.body.classList.remove('background-changed');
        }, 500);
    };
    
    img.onerror = function() {
        console.error('背景图片加载失败:', background.file);
        backgroundConfig.isLoading = false;
        
        if (showLoading) {
            showBackgroundLoading(false);
        }
        
        showError(`背景图片加载失败: ${background.name}`);
    };
    
    img.src = background.file;
}

// 切换背景
function changeBackground() {
    if (backgroundConfig.isLoading) return;
    
    let nextIndex = 0;
    if (backgroundConfig.current) {
        const currentIndex = backgroundConfig.images.findIndex(bg => bg.file === backgroundConfig.current.file);
        nextIndex = (currentIndex + 1) % backgroundConfig.images.length;
    }
    
    setBackground(nextIndex, true);
}

// 显示背景信息
function showBackgroundInfo() {
    const current = backgroundConfig.current;
    if (!current) return;
    
    const message = `当前背景: ${current.name}\n图片路径: ${current.file}\n双击可切换到下一张背景`;
    
    // 创建自定义信息框
    const infoBox = document.createElement('div');
    infoBox.className = 'bg-info-modal';
    infoBox.innerHTML = `
        <div class="bg-info-content">
            <div class="bg-info-header">
                <h4><i class="fas fa-image"></i> 背景信息</h4>
                <button class="bg-info-close" onclick="this.parentNode.parentNode.parentNode.remove()">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="bg-info-body">
                <div class="bg-info-item">
                    <strong>当前背景:</strong> ${current.name}
                </div>
                <div class="bg-info-item">
                    <strong>图片文件:</strong> ${current.file.split('/').pop()}
                </div>
                <div class="bg-info-item">
                    <strong>主题色:</strong> 
                    <span class="color-preview" style="background-color: ${current.color}"></span>
                    ${current.color}
                </div>
                <div class="bg-info-actions">
                    <button class="info-action-btn" onclick="changeBackground(); this.parentNode.parentNode.parentNode.parentNode.remove();">
                        <i class="fas fa-forward"></i> 下一张
                    </button>
                    <button class="info-action-btn" onclick="setRandomBackground(); this.parentNode.parentNode.parentNode.parentNode.remove();">
                        <i class="fas fa-random"></i> 随机
                    </button>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(infoBox);
    
    // 点击外部关闭
    infoBox.addEventListener('click', function(e) {
        if (e.target === infoBox) {
            infoBox.remove();
        }
    });
    
    // 3秒后自动关闭
    setTimeout(() => {
        if (infoBox.parentNode) {
            infoBox.remove();
        }
    }, 5000);
}

// 更新背景信息显示
function updateBackgroundInfo() {
    const current = backgroundConfig.current;
    if (!current) return;
    
    // 更新头部背景信息
    const bgInfoText = document.getElementById('bgInfoText');
    if (bgInfoText) {
        bgInfoText.textContent = current.name;
    }
    
    // 更新页脚背景信息
    const currentBgInfo = document.getElementById('currentBgInfo');
    if (currentBgInfo) {
        currentBgInfo.textContent = `当前背景: ${current.name}`;
    }
}

// 预加载所有背景图片
function preloadBackgroundImages() {
    backgroundConfig.images.forEach((background, index) => {
        const img = new Image();
        img.onload = function() {
            console.log(`背景图片预加载完成: ${background.name}`);
        };
        img.onerror = function() {
            console.warn(`背景图片预加载失败: ${background.name} (${background.file})`);
        };
        img.src = background.file;
    });
}

// 显示/隐藏背景加载状态
function showBackgroundLoading(show) {
    const bgLoading = document.getElementById('bgLoading');
    if (bgLoading) {
        bgLoading.style.display = show ? 'flex' : 'none';
    }
}

// 快速查询功能
function quickSearch(studentId) {
    const studentIdInput = document.getElementById('studentId');
    if (studentIdInput) {
        studentIdInput.value = studentId;
        updateSearchButtonState();
        searchGrade();
    }
}

// 双击背景切换功能
document.addEventListener('dblclick', function(e) {
    // 如果双击的不是输入框或按钮，则切换背景
    if (!e.target.closest('input, button, .result-container, .search-container')) {
        changeBackground();
    }
});

// 打印结果功能
function printResult() {
    window.print();
}

// 显示成功信息
function showSuccess(message) {
    const successDiv = document.createElement('div');
    successDiv.className = 'success-toast';
    successDiv.innerHTML = `
        <i class="fas fa-check-circle"></i>
        <span>${message}</span>
    `;
    
    document.body.appendChild(successDiv);
    
    requestAnimationFrame(() => {
        successDiv.classList.add('show');
    });
    
    setTimeout(() => {
        successDiv.classList.remove('show');
        setTimeout(() => {
            if (successDiv.parentNode) {
                successDiv.parentNode.removeChild(successDiv);
            }
        }, 300);
    }, 3000);
}
