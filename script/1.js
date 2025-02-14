// {% extends 'templates/base/manage_center.html' %}
// {% load static %}
// {% block css %}
// <link rel="stylesheet" href="{% static 'web/css/file.css' %}" />
// {% endblock %}
//
// {% block content %}
// <div class="container-fluid">
//     <div class="panel panel-warning" style="margin-top: 25px">
//         <div class="panel-heading">
//             <!-- 添加导航路径 -->
//             <div class="breadcrumb file-header-left" style="margin: 0; padding: 0; background-color: transparent;">
//                 <a href="{% url 'web:file' project_id=request.bugtracer.project.id %}" class="btn btn-link">
//                     <i class="fa fa-home" aria-hidden="true"></i> 根目录
//                 </a>
//                 {% for item in breadcrumb_list %}
//                 <a href="{% url 'web:file' project_id=request.bugtracer.project.id %}?folder_id={{ item.id }}"
//                     class="btn btn-link">
//                     <i class="fa fa-caret-right"></i> {{ item.name }}
//                 </a>
//                 {% endfor %}
//             </div>
//
//
//
//
//
//
//
//             <div class="file-header-right">
//
//                 <div class="btn-group">
//                     <!-- 上传文件按钮 -->
//                     <!-- 隐藏原生的文件输入框 -->
//                     <input type="file" name="uploadFile" id="uploadFile" style="display: none;" multiple />
//                     <!-- 创建一个美化的按钮,这样用户看到的是美化的按钮，但实际操作的是原生的文件选择框 -->
//                     <button class="btn btn-primary" onclick="document.getElementById('uploadFile').click()">
//                         <i class="fa fa-upload"></i> 上传文件
//                     </button>
//                     <!-- 新建文件夹按钮 -->
//                     <a type="button" data-toggle="modal" data-target="#add_edit_modal" data-whatever="新建文件夹"
//                         data-parent_id="{{ request.GET.folder_id }}" class="btn btn-success">
//                         <i class="fa fa-plus-circle"></i>新建文件夹
//                     </a>
//                 </div>
//             </div>
//         </div>
//         <table class="table">
//             <thead>
//                 <tr>
//                     <th>名称</th>
//                     <th>类型</th>
//                     <th>大小</th>
//                     <th>修改日期</th>
//                     <th>操作</th>
//                 </tr>
//             </thead>
//             <tbody>
//                 {% for item in file_list %}
//                 <tr>
//                     <td>
//                         {% if item.file_type == 1 %}
//                         <i class="fa fa-file" style="background-color: #AEAEAE"></i>
//                         {{ item.name }}
//                         {% else %}
//                         <a href="{% url 'web:file' project_id=request.bugtracer.project.id %}?folder_id={{ item.id }}">
//                             <i class="fa fa-folder" style="color: #b58900"></i>
//                             {{ item.name }}
//                         </a>
//
//                         {% endif %}
//
//                     </td>
//                     <td>
//                         {% if item.file_type == 1 %}
//                         {{ item.file_extension }}
//                         {% else %}
//                         文件夹
//                         {% endif %}
//                     </td>
//                     <td>
//                         {% if item.file_type == 1 %}
//                             {{ item.file_size }}KB
//
//
//                         {% endif %}
//                     </td>
//                     <td>{{ item.update_datetime }}</td>
//                     <td>
//                         <!--HTML中，id必须是唯一的,由于该a标签是循环生成的，因此不能设置id值 -->
//                         {% if item.file_type == 1 %}
//                             <a class="btn btn-success btn-xs download-btn" data-key="{{ item.key }}" data-name="{{ item.name }}">
//                                 <i class="fa fa-download"></i>下载
//                             </a>
//
//                         {% endif %}
//                                 <a class="btn btn-primary btn-xs" data-toggle="modal" data-target="#add_edit_modal"
//                             data-whatever="编辑文件/文件夹" data-folder-id="{{ item.id }}" data-folder-name="{{ item.name }}">
//                             <i class="fa fa-edit"></i>编辑
//                         </a>
//
//                         <a class="btn btn-danger btn-xs delete_btn" data-toggle="modal" data-target="#deleteModal"
//                             data-id="{{ item.id }}" data-name="{{ item.name }}">
//                             <i class="fa fa-trash"></i>删除
//                         </a>
//                     </td>
//                 </tr>
//                     {% endfor %}
//             </tbody>
//         </table>
//     </div>
// </div>
// <div class="modal fade" id="add_edit_modal" tabindex="-1" role="dialog">
//     <div class="modal-dialog" role="document">
//         <div class="modal-content">
//             <div class="modal-header">
//                 <button type="button" class="close" data-dismiss="modal">
//                     <span>&times;</span>
//                 </button>
//                 <h4 class="modal-title" id="myModalLabel"></h4>
//             </div>
//             <div class="modal-body">
//                 <form>
//                     {% csrf_token %}
//                     <!-- 在编辑文件夹时，我们会把当前文件夹的 ID 存储在隐藏表单中， -->
//                     <!-- name属性通常是在服务器端通过 request.POST.get('folderId') 获取值时使用的键名
//                         如果使用 AJAX 手动构建数据发送（而不是表单自动提交），确实可以省略 name 属性-->
//                     {# <input type="hidden" id="folderId" name="folderId">#}
//                     <input type="hidden" id="folderId">
//                     <!--添加隐藏的父文件夹ID字段-->
//                     <input type="hidden" id="parentId">
//                     {% for field in form %}
//                     <div class="form-group">
//                         <label for="{{ field.id_for_label }}">{{ field.label }}</label>
//                         {{ field }}
//                         <span class="error-msg"></span>
//                     </div>
//                     {% endfor %}
//                 </form>
//             </div>
//             <div class="modal-footer">
//                 <button type="button" class="btn btn-default" data-dismiss="modal">取消</button>
//                 <button type="button" class="btn btn-primary" id="submit_btn">确定</button>
//             </div>
//         </div>
//     </div>
// </div>
// <!-- 删除确认模态框 -->
// <div class="modal fade" id="deleteModal" tabindex="-1" role="dialog">
//     <div class="modal-dialog" role="document">
//         <div class="modal-content">
//             <div class="modal-header">
//                 <button type="button" class="close" data-dismiss="modal">
//                     <span>&times;</span>
//                 </button>
//                 <h4 class="modal-title">
//                     <i class="fa fa-exclamation-triangle text-warning"></i>
//                     提示
//                 </h4>
//             </div>
//             <div class="modal-body">
//                 <div>
//                     确定要删除文件夹 "<span id="folderToDelete"></span>" 吗？
//                 </div>
//             </div>
//             <div class="modal-footer">
//                 <button type="button" class="btn btn-default" data-dismiss="modal">取消</button>
//                 <button type="button" class="btn btn-danger" id="confirmDelete">
//                     <i class="fa fa-trash"></i> 确定删除
//                 </button>
//             </div>
//         </div>
//     </div>
// </div>
// {% endblock %}
// {% block js %}
// <script src="{% static 'web/js/http_gosspublic.alicdn.com_aliyun-oss-sdk-6.17.1.min.js' %}"></script>
// <script>
//     const file_add_url = "{% url 'web:file_add' project_id=request.bugtracer.project.id %}";
//     const file_edit_url = "{% url 'web:file_edit' project_id=request.bugtracer.project.id %}";
//     const file_delete_url = "{% url 'web:file_delete' project_id=request.bugtracer.project.id %}";
//     $(function () {
//         initmodal();  // 根据触发按钮改变模态内容
//         bindAddEditFolder();  // 绑定新建添加文件夹事件
//         bindDeleteFolder();  // 绑定删除文件夹事件
//         bindDownloadFile();  // 绑定下载文件事件
//     })
//
//     function initmodal() {
//         // 监听ID为'add_edit_modal'的模态框的显示事件
//         $('#add_edit_modal').on('show.bs.modal', function (event) {
//             // 获取当前模态框的jQuery对象
//             let modal = $(this)
//             // 获取触发模态框的元素（通常是按钮）
//             let button = $(event.relatedTarget)
//
//             // 获取数据（当前点击按钮所操作文件夹的数据）
//             let recipient = button.data('whatever')
//             let folderId = button.data('folder-id');  // 编辑的文件夹/文件ID
//             let folderName = button.data('folder-name');  // 编辑的文件夹/文件名称
//             let parentId = button.data('parent_id')  // 新建时的父文件夹ID
//
//             // 设置模态框标题
//             modal.find('.modal-title').text(recipient)
//             // 重置表单（获取jQuery对象（所有的form元素）中的第一个原生DOM元素）
//             modal.find('form')[0].reset();
//             // 清除错误信息
//             modal.find('.error-msg').text('');
//
//             if (folderId) {  // 编辑模式
//                 modal.find('#folderId').val(folderId);  // 将ID存储在隐藏字段中
//                 modal.find('#id_name').val(folderName);  // 设置name字段输入框的值为当前文件夹/文件的名称
//             } else {  // 新建模式
//                 modal.find('#folderId').val('');
//                 modal.find('#id_name').val('');
//                 // 保存父文件夹ID
//                 modal.find('#parentId').val(parentId)
//             }
//
//         })
//     }
//
//     function bindAddEditFolder() {
//         $('#submit_btn').click(function () {
//             let folderId = $('#folderId').val() || ''; // 获取在隐藏字段中的ID
//             let url = folderId ? file_edit_url : file_add_url;  // 当前请求地址
//             let method = folderId ? 'PUT' : 'POST';  // 编辑模式：PUT，新增模式：POST
//
//             // 根据请求类型决定如何处理数据
//             let ajaxOptions = {
//                 url: url,
//                 type: method,
//                 headers: {
//                     // 添加 CSRF 令牌
//                     "X-CSRFToken": $('[name="csrfmiddlewaretoken"]').val()
//                 },
//                 dataType: "json",
//                 success: function (data) {
//                     if (data.status) {
//                         $('#add_edit_modal').modal('hide');
//                         window.location.reload();
//                     } else {
//                         $.each(data.error, function (key, value) {
//                             $("#id_" + key).next().text(value[0]);
//                         })
//                     }
//                 }
//             };
//
//             if (method === 'PUT') {
//                 // PUT 请求时构造 JSON 数据
//                 ajaxOptions.headers["Content-Type"] = "application/json";  // 设置请求体中的数据格式为JSON
//                 ajaxOptions.data = JSON.stringify({  // 将数据转换为JSON字符串
//                     'folderId': folderId,
//                     'name': $('#id_name').val() || ''
//                 });
//             } else {
//                 // POST 请求时使用表单数据
//                 let formData = new FormData();  // 创建 FormData 对象
//                 formData.append('name', $('#id_name').val() || '');  // 将表单中的name字段值添加到FormData对象中
//                 formData.append('parent', $('#parentId').val() || '');  // 将父文件夹ID添加到FormData对象中
//                 ajaxOptions.data = formData;  // 配置ajaxOptions，设置data为FormData对象
//                 // POST 请求不需要设置 Content-Type，让浏览器自动处理数据格式
//                 ajaxOptions.processData = false;
//                 ajaxOptions.contentType = false;
//             }
//             $.ajax(ajaxOptions);
//         })
//     }
//
//     function bindDeleteFolder() {
//         let deleteId = null;
//
//         // 点击删除按钮
//         $('.delete_btn').click(function () {
//             deleteId = $(this).data('id');  // 获取当前删除的文件夹/文件的ID
//             // 添加前端验证(提供更好的用户体验，并减少无效请求发送到服务器)
//             if (!deleteId) {
//                 showMessageDelete('error', '无效的文件/文件夹ID');
//                 return;
//             }
//             $('#folderToDelete').text($(this).data('name'));  // 设置要删除的文件夹/文件的名称
//             // 移除了重复的 modal('show') 调用，因为 Bootstrap 的 data-toggle="modal" 已经会处理模态框的显示
//             // $('#deleteModal').modal('show');
//         });
//
//         // 确认删除
//         $('#confirmDelete').click(function () {
//             // $btn 是一个 jQuery 对象，它引用了当前被选中的按钮元素
//             // 禁用当前按钮，并将按钮文本更改为带有旋转图标的“删除中...”
//             let $btn = $(this).prop('disabled', true)
//                 .html('<i class="fa fa-spinner fa-spin"></i> 删除中...');
//
//             $.ajax({
//                 url: file_delete_url,
//                 type: 'POST',
//                 data: {
//                     'folderId': deleteId,
//                     'csrfmiddlewaretoken': '{{ csrf_token }}'
//                 },
//                 success: function (res) {
//                     if (res.status) {
//                         $('#deleteModal').modal('hide');
//                         showMessageDelete('success', '删除成功');
//                         // 让用户能看到"删除成功"的提示消息（如果立即刷新页面，提示消息可能还没来得及看到就消失了）
//                         setTimeout(() => window.location.reload(), 1500);
//                     } else {
//                         showMessageDelete('error', res.error || '删除失败');
//                         $btn.prop('disabled', false)
//                             .html('<i class="fa fa-trash"></i> 确定删除');
//                     }
//                 }
//             });
//         });
//     }
//
//     // 删除消息提示
//     function showMessageDelete(type, msg) {
//         // 1. 根据type参数决定使用哪个图标和样式类
//         let icon = type === 'success' ? 'check-circle' : 'times-circle';  // 设置图标(对钩：叉号)
//         let alertClass = type === 'success' ? 'success' : 'danger';  // 设置样式（红色：绿色）
//         // left: 50% - 将元素的左侧定位到视窗宽度的50%处
//         // transform: translateX(-50%) - 只在X轴（水平方向）上向左移动自身宽度的50%
//         // .appendTo('body')：将消息框添加到页面
//         // .delay(1500)：停留1.5秒
//         // .fadeOut()：使用淡出动画效果
//         // .remove()：动画完成后删除元素
//         $(`<div class="alert alert-${alertClass}" style="position: fixed; top: 30px; left: 50%;
// transform: translateX(-50%); text-align: center; z-index: 9999;">
// <i class="fa fa-${icon}"></i> ${msg}
// </div>`).appendTo('body').delay(1500).fadeOut(function () {
//             $(this).remove();
//         });
//     }
//
//     // 文件上传处理
//     $('#uploadFile').change(async function (e) {  // 当用户选择文件时，触发文件输入框的 change 事件,执行异步函数处理文件上传逻辑
//         const files = Array.from(e.target.files);  // ：e.target.files 返回的是一个 FileList 对象，而不是一个真正的数组。虽然 FileList 对象可以像数组一样访问其元素，但它不支持数组的所有方法
//         if (!files.length) return;  // 如果没有选择文件，直接返回
//
//         // 获取项目配置（从Django模板变量获取）
//         const maxSingleFileMB = parseInt("{{ request.bugtracer.project.leader.member_level.single_file_space }}", 10) || 0;
//         const remainSpaceKB = parseInt("{{ request.bugtracer.project.remain_space }}", 10) || 0;
//         // 添加验证以确保值有效
//         if (!maxSingleFileMB || !remainSpaceKB) {
//             showMessageUpload('error', '无法获取项目配置信息');
//             this.value = '';  // 清空文件选择
//             return;
//         }
//
//         // 执行校验
//         const res = validateFilesBeforeUpload(files, maxSingleFileMB, remainSpaceKB);
//         const validationFiles = res.validFiles;
//         if (!res.valid) {
//             showMessageUpload('error', res.message);
//             if (!validationFiles.length) {  // 如果合法文件数组为空，则清空文件选择框的值，并返回
//                 this.value = '';
//                 return;
//             }
//         }
//
//         try {
//             // 显示总进度条
//             if (validationFiles.length) {
//                 const totalSize = validationFiles.reduce((sum, file) => sum + file.size, 0);  // reduce方法遍历 files 数组，累加每个文件的大小，0是表示累加器sum的初始状值,
//                 let uploadedSize = 0;  // 初始化已上传文件大小为 0(根据Web API的标准，File对象的size属性返回的是文件的字节数，单位是字节（bytes）)
//                 showMessageUpload('info', `准备上传 ${files.length} 个文件（${formatSize(totalSize)}）`);  // 告知用户即将上传的文件数量及总大小
//
//                 // 获取OSS凭证
//                 const credentials = await fetchCredentials();
//                 if (!credentials) return;
//
//                 // 初始化OSS客户端
//                 const client = new OSS(credentials.config);
//
//                 // 上传文件(第一层：文件选择后的回调)
//                 const uploadPromises = validationFiles.map(file =>  // 遍历文件列表，为每个文件创建上传任务,每个上传任务会调用 uploadFile 函数，并传递一个回调函数用于更新进度
//                     // (第二层：为每个文件创建上传任务时的回调)
//                     uploadFile(file, client, (progress) => {
//                         uploadedSize += progress.loaded;  // 更新已上传文件大小
//                         const percent = Math.round((uploadedSize / totalSize) * 100);  // 计算上传进度百分比并四舍五入
//                         showTotalProgress(percent, `${formatSize(uploadedSize)}/${formatSize(totalSize)}`);  // 显示当前进度和已上传/总文件大小
//                     })
//                 );
//
//                 // 等待所有上传完成
//                 const uploadResults = await Promise.allSettled(uploadPromises);  // Promise.allSettled会等待所有的Promise执行完毕，不论成功或失败，返回一个包含所有结果的数组
//
//                 // 收集成功结果
//                 const successFiles = uploadResults
//                     .filter(r => r.status === 'fulfilled' && r.value)  // 使用filter方法筛选出状态为'fulfilled'且有值的结果
//                     .map(r => r.value);  // 使用map方法提取筛选结果中的值
//
//                 // 批量保存到数据库
//                 const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));  // 创建一个延迟函数（Promise 方式实现）
//                 if (successFiles.length) {
//                     const saveResult = await bulkSaveFiles(successFiles);
//                     if (saveResult.status) {
//                         // 等待1.5秒
//                         await delay(1500);
//                         // 显示保存成功消息
//                         showMessageUpload('success', `成功保存 ${successFiles.length} 个文件`);
//                         // 再等待1秒
//                         await delay(1000);
//                         // 刷新页面
//                         window.location.reload();
//                     }
//                 }
//             }
//         } catch (err) {
//             showMessageUpload('error', `上传失败: ${err.message}`);
//         }
//     });
//
//     // 辅助函数：文件容量校验
//     function validateFilesBeforeUpload(files, maxSingleFileMB, remainSpaceKB) {
//         const maxSingleFileBytes = maxSingleFileMB * 1024 * 1024;
//         const maxTotalBytes = remainSpaceKB * 1024;
//
//         // 总容量校验
//         const totalSize = files.reduce((sum, file) => sum + file.size, 0);
//         if (totalSize > maxTotalBytes) {
//             return {
//                 valid: false,
//                 validFiles: [],  // 返回一个空数组，表示没有合法的文件
//                 message: `所选文件总大小超过剩余空间（剩余：${formatSize(maxTotalBytes)}）`
//             };
//         }
//
//         // 单文件校验
//         const invalidFiles = files.filter(file => file.size > maxSingleFileBytes);
//         if (invalidFiles.length) {
//             return {
//                 valid: false,
//                 validFiles: files.filter(file => file.size <= maxSingleFileBytes),
//                 message: `以下文件超过${maxSingleFileMB}MB限制：${invalidFiles.map(f => f.name).join(', ')}`
//             };
//         }
//
//
//         // 同名文件校验（仅检查文件名，排除文件夹）
//         const existingFiles = Array.from(document.querySelectorAll('.table tbody tr'))
//             .filter(tr => {
//                 // 通过图标类型判断是否是文件（文件夹图标为 fa-folder，文件图标为 fa-file）
//                 return tr.querySelector('.fa-file');
//             })
//             .map(tr => {
//                 // 获取文件名称（直接取第一个td的text内容，并过滤掉图标字符）
//                 const td = tr.querySelector('td:first-child');
//                 return Array.from(td.childNodes)
//                     .filter(node => node.nodeType === Node.TEXT_NODE)
//                     .map(node => node.textContent.trim())
//                     .join('')
//                     .replace(/^\s+|\s+$/g, '');
//             });
//
//         const { validFiles, conflictFiles } = files.reduce((acc, file) => { // reduce快速分类合法以及不合法文件
//             existingFiles.includes(file.name) ?
//                 acc.conflictFiles.push(file.name) :
//                 acc.validFiles.push(file);
//             return acc;
//         }, { validFiles: [], conflictFiles: [] });
//
//         if (conflictFiles.length) {
//             return {
//                 valid: false,
//                 validFiles: validFiles,
//                 message: `将跳过以下 ${conflictFiles.length} 个重名文件：【${conflictFiles.join(' , ')}】`
//             };
//         }
//         return {
//             valid: true,
//             validFiles: files
//         };
//     }
//
//     // 辅助函数：获取OSS凭证
//     async function fetchCredentials() {
//         try {
//             // 向后端请求阿里云OSS的临时访问凭证
//             /*
//                 await fetch(url, options) 发起一个到指定 URL 的 HTTP 请求。
//                 await 关键字确保代码会等待 fetch 请求完成并返回响应，然后再继续执行后续代码。
//                 fetch 返回一个 Promise，await 会暂停当前函数的执行，直到 Promise 被解决（resolve）或拒绝（reject），从而获取到最终的响应结果
//             */
//             const res = await fetch(`{% url 'web:file_credentials' project_id=request.bugtracer.project.id %}`);
//             // 解构响应数据获取状态、凭证数据和错误信息
//             const { status, data, error } = await res.json();
//
//             // 如果临时凭证获取失败，显示错误消息并返回
//             if (!status) {
//                 showMessageUpload('error', error || '获取上传凭证失败');
//                 return;
//             }
//
//             return {
//                 config: {
//                     accessKeyId: data.accessKeyId,
//                     accessKeySecret: data.accessKeySecret,
//                     stsToken: data.securityToken,  // 注意这里是stsToken
//                     region: data.region.startsWith('oss-') ? data.region : `oss-${data.region}`,  // 确保region格式为oss-{regionId}（如oss-cn-hangzhou）
//                     bucket: data.bucket,
//                     secure: true  // 使用HTTPS协议
//                 },
//             };
//         } catch (err) {
//             showMessageUpload('error', err.message);
//             return null;
//         }
//     }
//
//     // 辅助函数：oss文件上传
//     async function uploadFile(file, client, onProgress) {
//         try {
//             const key = `${Date.now()}-${file.name}`;  // 生成OSS中的文件存储路径（注意是否符合阿里云oss的key规范）
//             let lastLoaded = 0;
//
//             const result = await client.multipartUpload(key, file, {
//                 // (第三层：OSS上传进度的回调)
//                 progress: (p) => {  // p是0到1之间的小数,表示上传进度
//                     const loaded = p * file.size;  // 计算实际已上传的字节数
//                     const delta = loaded - lastLoaded;  // 计算本次上传的增量字节
//                     lastLoaded = loaded;  // 更新lastLoaded为当前已上传量
//
//                     // 调用外部传入的进度回调函数
//                     onProgress({
//                         loaded: delta,  // 新上传的字节数
//                         name: file.name,  // 文件名
//                         percent: Math.floor(p * 100)  // 当前文件的上传百分比
//                     });
//                 }
//             });
//
//             return {
//                 name: file.name,
//                 key: result.name,
//                 size: file.size,
//                 type: file.type
//             };
//         } catch (err) {
//             showMessageUpload('error', `${file.name} 上传失败: ${err.message}`);
//             return null;
//         }
//     }
//
//     // 辅助函数：批量保存
//     async function bulkSaveFiles(files) {
//
//         const folder_id = new URLSearchParams(window.location.search).get('folder_id') || '';
//         const formData = new FormData();
//
//         formData.append('files', JSON.stringify(files));  // 浏览器FormData的append()方法只能处理字符串或Blob/File对象
//         formData.append('parent', folder_id);
//
//         const res = await fetch("{% url 'web:file_bulk_upload' project_id=request.bugtracer.project.id %}", {
//             method: 'POST',
//             headers: {
//                 'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
//             },
//             body: formData
//         });
//
//         const data = await res.json();  // 添加响应解析
//
//         if (!data.status) {
//             showMessageUpload('error', `保存失败: ${data.error}`);
//             return { status: false };
//         }
//         return { status: true };
//     }
//
//     // 辅助函数：显示进度条
//     function showTotalProgress(percent, text) {
//         const validPercent = isNaN(percent) ? 0 : percent;  // 确保percent是有效数字
//         const progressId = 'total-upload-progress';
//
//         // 检查是否已存在进度条
//         let progressBar = $(`#${progressId}`);
//
//         if (progressBar.length === 0) {
//             // 创建进度条HTML
//             const progressHtml = `
//                     <div id="${progressId}" class="upload-progress" style="position: fixed; top: 30px; left: 50%; transform: translateX(-50%);
//                         width: 300px; background: white; border-radius: 4px; box-shadow: 0 2px 5px rgba(0,0,0,0.2);
//                         padding: 10px; z-index: 9999;">
//                         <div style="margin-bottom: 5px; display: flex; justify-content: space-between; align-items: center;">
//                             <span class="progress-status">
//                                 <i class="fa fa-upload"></i> 正在上传
//                             </span>
//                             <span class="progress-text"></span>
//                         </div>
//                         <div style="background-color: #f5f5f5; height: 20px; border-radius: 10px; overflow: hidden;">
//                             <div class="progress-bar" style="width: 0; height: 100%;
//                                 background-color: #007bff;
//                                 transition: width 0.3s ease-in-out;">
//                             </div>
//                         </div>
//                     </div>
//                 `;
//             progressBar = $(progressHtml).appendTo('body');
//         }
//
//
//         // 更新进度条
//         const $bar = progressBar.find('.progress-bar');
//         const $status = progressBar.find('.progress-status');
//         const $text = progressBar.find('.progress-text');
//
//         // 更新进度文本
//         $text.text(`${validPercent}% ${text}`);
//
//         // 更新进度条宽度
//         $bar.css('width', `${validPercent}%`);
//
//         // 当上传完成时
//         if (validPercent === 100) {
//             // 更新状态图标和颜色
//             $status.html('<i class="fa fa-check-circle" style="color: #28a745;"></i> 上传完成');
//             $bar.css('background-color', '#28a745');
//
//             // 1.5秒后移除进度条并显示完成消息
//             setTimeout(() => {
//                 progressBar.fadeOut(() => {
//                     progressBar.remove();
//                 });
//             }, 1500);
//         }
//     }
//
//     // 辅助函数：消息提示函数
//     function showMessageUpload(type, msg) {
//
//         // 移除已存在的提示
//         $('.alert-message').remove();
//
//         // 配置提示样式
//         const config = {
//             success: { icon: 'check-circle', class: 'success' },
//             error: { icon: 'times-circle', class: 'danger' },
//             info: { icon: 'info-circle', class: 'info' }
//         }[type] || { icon: 'info-circle', class: 'info' };
//
//
//         // 创建提示元素
//         const alert = $(`
//                 <div class="alert alert-${config.class} alert-message"
//                      style="position: fixed; top: 30px; left: 50%; transform: translateX(-50%);
//                             z-index: 9999; padding: 10px 20px; border-radius: 4px;">
//                     <i class="fa fa-${config.icon}"></i> ${msg}
//                 </div>
//             `).appendTo('body');
//
//         // 如果是成功或错误提示，自动消失
//         if (type !== 'info') {
//             alert.delay(3000).fadeOut(() => alert.remove());
//         }
//     }
//
//     // 辅助函数：格式化文件大小
//     function formatSize(bytes) {
//         const units = ['B', 'KB', 'MB', 'GB'];  // 定义单位数组：
//         let size = bytes;  // size 变量用于存储当前的文件大小，初始值为传入的 bytes
//         let unitIndex = 0;  // unitIndex 用于记录当前文件的单位索引，初始值为 0
//         while (size >= 1024 && unitIndex < units.length - 1) {
//             size /= 1024;
//             unitIndex++;
//         }
//         return `${size.toFixed(1)}${units[unitIndex]}`;
//     }
//
//     // 下载文件处理函数
// async function bindDownloadFile() {
//     $('.download-btn').click(async function() {
//         const key = $(this).data('key');
//         const fileName = $(this).data('name');
//
//         try {
//             // 获取OSS凭证
//             const credentials = await fetchCredentials();
//             if (!credentials) return;
//
//             // 初始化OSS客户端
//             const client = new OSS(credentials.config);
//
//             // 生成文件下载链接（签名URL，有效期1小时）
//             const signedUrl = client.signatureUrl(key, {
//                 expires: 3600,  // 链接有效期1小时
//                 response: {
//                     'content-disposition': `attachment; filename=${encodeURIComponent(fileName)}`  // 指定下载时的文件名
//                 }
//             });
//
//             // 创建一个隐藏的a标签来触发下载
//             const link = document.createElement('a');
//             link.href = signedUrl;
//             link.download = fileName;
//             document.body.appendChild(link);
//             link.click();
//             document.body.removeChild(link);
//
//         } catch (err) {
//             showMessageUpload('error', `下载失败: ${err.message}`);
//         }
//     });
// }
// </script>
// {% endblock %}