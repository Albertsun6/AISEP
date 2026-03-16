这里是我的想法，先不用参考，需要的时候我会说

（完成）增加多项目管理
增加一个对现有系统的逆向管理，从代码，文档，前端，增加多项目管理，
进化 
根据现有系统日志及数据发现需求
参考上下文工程建立目录
有个项目是openspec和speckit，借鉴一下他们的文件组织形式
自动发现问题，
上下文管理（控制长度）
上下文用完无关即归档，比如slice不同阶段之间
把sces 改为 AISEP
适当的时机引入 ADR（Architecture Decision Record）
模板是不是可以根据项目类型按需加载
在做的过程中要提升认知，AI给学习笔记
每次项目结束，整理经验，进化 分层
探讨给使用aisep用户的呈现形式
随着完善和项目越来越多，如何控制文件体积，为了节省上下文，不关注的项目不要加载
Aider, Continue  allure-report、coverage-report、test-report、htmlcov

增加github 代码管理

有趣的融合可能：如果未来 AISEP 做了 VS Code Extension（方案 C 第三步），完全可以把 Continue 的 Context Provider 架构作为技术底座——让 AISEP 的 Workflow 和 Skills 通过 Continue 的插件机制暴露给 LLM。

研究 Continue 的 Context Provider 源码 — 看看它的声明式上下文注册怎么实现的

AI 自主判断 + 事后审计            → 🤖 全自动（远期） 这个好，结合进化机制
遇到简写要给个全称，比如NLP(Natural Language Processing)
写一个关于这个系统的论文，整个过程，实现方式，探索发现
短期、中期、长期 记忆管理

标准的工作方法，流程，在每次做的时候都遵循，比如探索
如何把runtime 沉淀成静态文件
是否可以借鉴使用plantir公司 的本体论方式 组织信息
不会做，先思考学习，从做中整理方法，方法论，沉淀成skill，完善
A2A 自进化，多个agent针对一个话题探讨，人审核
antigravity，cursor 等coding agent原理
列式存储（Parquet/Spark）+ 索引层 + 关系物化
/reserch 是不是应该把gemimi.md 和进化整合到系统中

把 / command 注册到antigrvity 对话中，我输入斜杠给我命令提示，现在没有

/deepdive，研究一下，在项目执行过程中和之后要再哪里增加deepdive，以便系统自我完善

学crewAI autogen优点，放到aisep中，
是不是应该保留一份born 的0系统，就像出生一样，只带基因，进化可以有不同的分支
项目命名要有意义，不然不好找
做个许愿池，整理我的想法，帮我整理许愿池，研究许愿池制定计划，我审批，执行
是否可以分Agent，三省六部制
后期我们是不是可以从0训练一个我们自己的模型
增加全自动进化模式，从born开始训练
系统框架升级 试点odoo

应该有个找和我们项目相关最新资料和论文的agent，不断找好东西为我们所用，海绵宝宝，黑洞

增加对系统的健康扫描和优化建议，体检，命令，定时，或人工
借鉴世界模型，预测
结束时发声音提醒，读，老孙做完了，老孙，帮我一下    ...

你叫fiona，你也要有灵魂，加上 ，基因，灵魂

做系统分享ppt，包含介绍，亮点，实现过程，功能列表，使用方法，定期输出，做视频自动讲，放到youtube

walkthrough要永久保存，机制

deepdive 改成dive
项目的完整文档，给用户看，需求，设计，实施过程，经验，培训资料，改进建议。。。。

