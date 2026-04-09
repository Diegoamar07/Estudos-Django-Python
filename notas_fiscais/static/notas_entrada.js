// Usamos window.addEventListener para garantir que TUDO (inclusive o jQuery do Django) carregou
window.addEventListener('load', function() {
    (function($) {
        // Agora o $ funciona porque passamos o django.jQuery para ele
        $(document).ready(function() {
            
            // Usamos $(document).on para garantir que funcione mesmo em campos dinâmicos
            $(document).on('change', '#id_numero_oc', function() {
                let id_oc = $(this).val();
                
                if (id_oc) {
                    $.ajax({
                        url: "/get-oc-details/" + id_oc + "/",
                        success: function(data) {
                            $('.field-data_ordem .readonly').text(data.data_ordem);

                            // PEGA A DATA DE HOJE E INJETA NO CAMPO DATA_ENTRADA
                            let hoje = new Date().toLocaleDateString('pt-BR');
                            $('.field-data_entrada .readonly').text(hoje);

                            $('#id_fornecedor').val(data.fornecedor);
                            $('#id_grupo_fornec').val(data.grupo_fornec);
                            $('#id_produto').val(data.produto);
                            $('#id_unidade').val(data.unidade);
                            $('#id_preco_unitario').val(data.preco_unitario);
                            $('#id_quantidade').val(data.quantidade);
                            $('#id_status').val('FECHADO').trigger('change');                        
                            $('#id_total_nota').val(data.total_oc).attr('readonly', true);                        },
                        error: function() {
                            console.error("Erro na requisição AJAX");
                        }
                    });
                }
            });
        });
    })(django.jQuery); 
}); 
