/**
 * Created by bradleyt on 21/11/2017.
 */

$(document).ready(function() {
    $(':input[species$=continent]').on('change', function() {
        var prefix = $(this).getFormPrefix();
        $(':input[name=' + prefix + 'test]').val(null).trigger('change');
    });
});
~       
