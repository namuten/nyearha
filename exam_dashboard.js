// JS for Exam Dashboard (Interactive Quiz Setup)

const subjectFiles = [
    { id: 'sci', title: '통합과학1', file: 'step3_통합과학1_문제.md', icon: '🌱' },
    { id: 'soc', title: '통합사회1', file: 'step3_통합사회1_문제.md', icon: '🧶' },
    { id: 'his', title: '한국사1', file: 'step3_한국사1_문제.md', icon: '🏺' },
    { id: 'math', title: '공통수학1', file: 'step3_공통수학1_문제.md', icon: '📐' },
    { id: 'eng', title: '공통영어1', file: 'step3_공통영어1_문제.md', icon: '🖍️' }
];

document.addEventListener('DOMContentLoaded', () => {
    const navMenu = document.getElementById('navMenu');
    const contentArea = document.getElementById('contentArea');
    const subjectTitle = document.getElementById('subjectTitle');

    // 왼쪽 사이드메뉴 생성
    subjectFiles.forEach(item => {
        const li = document.createElement('li');
        li.className = 'nav-item';
        li.innerHTML = `<span>${item.icon}</span> ${item.title}`;
        
        li.addEventListener('click', () => loadAndTransformMarkdown(item, li));
        navMenu.appendChild(li);
    });

    async function loadAndTransformMarkdown(item, listItem) {
        document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
        listItem.classList.add('active');
        subjectTitle.innerHTML = `${item.icon} ${item.title}`;
        contentArea.innerHTML = '<div style="text-align:center; padding:4rem;">문제지를 불러오는 중입니다 ☁️</div>';

        try {
            const response = await fetch(item.file + '?t=' + new Date().getTime());
            if (!response.ok) throw new Error('파일을 가져올 수 없습니다.');
            
            const markdownText = await response.text();
            const rawHtml = marked.parse(markdownText);
            
            // Transform HTML into Interactive Quiz UI
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = rawHtml;
            
            const interactiveDoc = document.createDocumentFragment();
            const elements = Array.from(tempDiv.children);
            
            let currentQContainer = null;
            
            elements.forEach(el => {
                // 문제 제목 (H3) 발견 시 새로운 컨테이너 개설
                if (el.tagName === 'H3' && el.textContent.includes('문제')) {
                    currentQContainer = document.createElement('div');
                    currentQContainer.className = 'question-container';
                    currentQContainer.appendChild(el.cloneNode(true));
                    
                    const optionsDiv = document.createElement('div');
                    optionsDiv.className = 'options-container';
                    currentQContainer.appendChild(optionsDiv);
                    
                    interactiveDoc.appendChild(currentQContainer);
                } 
                else if (currentQContainer) {
                    // 선택지(①~⑤) 추출
                    if (el.tagName === 'P' && el.innerHTML.includes('①')) {
                        const htmlStr = el.innerHTML;
                        let markers = ['①','②','③','④','⑤'];
                        let splitText = htmlStr;
                        // 매커니즘: 구분자 활용하여 옵션을 쪼갬
                        markers.forEach((m, idx) => {
                            splitText = splitText.replace(new RegExp(m, 'g'), `|||${idx+1}|||${m}`);
                        });
                        
                        const parts = splitText.split('|||');
                        
                        // 기호 앞의 잔여 텍스트가 있다면 일반 본문으로 추가
                        if (parts[0].trim() !== "") {
                            const pHead = document.createElement('p');
                            pHead.innerHTML = parts[0];
                            currentQContainer.insertBefore(pHead, currentQContainer.querySelector('.options-container'));
                        }
            
                        // 쪼개진 옵션들을 클릭 디브로 변환
                        const optContainer = currentQContainer.querySelector('.options-container');
                        for (let i = 1; i < parts.length; i += 2) {
                            const ansNum = parts[i];
                            const content = parts[i+1];
                            const optDiv = document.createElement('div');
                            optDiv.className = 'quiz-option';
                            optDiv.dataset.ans = ansNum;
                            // <br> 클린징
                            optDiv.innerHTML = content.replace(/<br\s*\/?>$/, '').trim(); 
                            optContainer.appendChild(optDiv);
                        }
                        return; // 스킵 원래 P 태그
                    }
                    
                    // 정답 해설 영역 (<details>) 파싱 및 버튼 교체
                    if (el.tagName === 'DETAILS') {
                        const detailsHtml = el.innerHTML;
                        let correctNumber = 0;
                        const match = detailsHtml.match(/>.*?(①|②|③|④|⑤)/) || detailsHtml.match(/(①|②|③|④|⑤)/);
                        if (match) {
                            const map = {'①':1, '②':2, '③':3, '④':4, '⑤':5};
                            correctNumber = map[match[1] || match[0]];
                        }
                        
                        const explanationBody = detailsHtml.replace(/<summary>.*?<\/summary>/s, '').trim();
                        
                        const interactiveArea = document.createElement('div');
                        interactiveArea.className = 'interactive-area';
                        interactiveArea.innerHTML = `
                            <div class="btn-wrap">
                                <button class="check-btn" data-correct="${correctNumber}">✔️ 정답 확인하기</button>
                            </div>
                            <div class="feedback-area" style="display:none;"></div>
                            <div class="explanation-area" style="display:none;">
                                <div class="expl-title">📝 정답 및 해설 ${match ? (match[1] || match[0]) : ''}</div>
                                <div class="expl-body">${explanationBody}</div>
                            </div>
                        `;
                        currentQContainer.appendChild(interactiveArea);
                        return; // 스킵 원래 details 태그
                    }
                    
                    currentQContainer.insertBefore(el.cloneNode(true), currentQContainer.querySelector('.options-container'));
                } 
                else {
                    interactiveDoc.appendChild(el.cloneNode(true)); // 머릿말 등 기타 요소
                }
            });
            
            contentArea.innerHTML = '';
            contentArea.appendChild(interactiveDoc);
            
            // MathJax 렌더링 호출
            if (window.MathJax) {
                window.MathJax.typesetPromise([contentArea]).catch(e => console.log(e));
            }
            
            // 옵션 클릭 및 정답확인 이벤트 위임
            contentArea.addEventListener('click', handleQuizInteraction);
            
        } catch (e) {
            console.error(e);
        }
    }

    // 퀴즈 인터랙션 로직
    function handleQuizInteraction(e) {
        // 1. 답안보기 (옵션 클릭)
        const opt = e.target.closest('.quiz-option');
        if (opt) {
            const qContainer = opt.closest('.question-container');
            if (qContainer.classList.contains('answered')) return; // 이미 제출된 건 변경 금지
            
            qContainer.querySelectorAll('.quiz-option').forEach(o => o.classList.remove('selected'));
            opt.classList.add('selected');
        }

        // 2. 정답 체킹 버튼 클릭
        const checkBtn = e.target.closest('.check-btn');
        if (checkBtn) {
            const qContainer = checkBtn.closest('.question-container');
            
            const selectedOpt = qContainer.querySelector('.quiz-option.selected');
            if (!selectedOpt) {
                alert('🎨 먼저 위의 보기 번호를 클릭하여 정답을 선택해주세요!');
                return;
            }
            
            qContainer.classList.add('answered'); // 잠금 처리
            
            const userAns = selectedOpt.dataset.ans;
            const correctAns = checkBtn.dataset.correct;
            
            const feedbackBox = qContainer.querySelector('.feedback-area');
            const explBox = qContainer.querySelector('.explanation-area');
            
            if (userAns === correctAns) {
                selectedOpt.classList.add('correct');
                feedbackBox.innerHTML = '🎉 <b>정답입니다!</b> 완벽해요.';
                feedbackBox.className = 'feedback-area success';
            } else {
                selectedOpt.classList.add('wrong');
                const realAnsObj = qContainer.querySelector(`.quiz-option[data-ans="${correctAns}"]`);
                if (realAnsObj) realAnsObj.classList.add('correct_reveal'); // 진짜 정답 형광펜 표시
                feedbackBox.innerHTML = '💡 <b>오답입니다.</b> 올바른 해설을 확인하고 다시 복습해보세요.';
                feedbackBox.className = 'feedback-area error';
            }
            
            // 영역 노출 및 버튼 숨김
            checkBtn.parentElement.style.display = 'none';
            feedbackBox.style.display = 'block';
            explBox.style.display = 'block';
        }
    }
});
