import os
import sys
from utils import table_transformer

## init OpenAI credentials
open_ai_api_key = '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'
os.environ["OPENAI_API_KEY"] = open_ai_api_key
        
if __name__=="__main__":
    tt = table_transformer()
    print('Creating cleaning agent')
    a1 = tt.create_agent(sys.argv[2])
    dups = tt.get_dup_columns(a1)
    dups_for_rem = tt.present_dups_for_removal(dups)
    if len(dups_for_rem)>0:
        print('Duplicate columns found.')
        print(dups_for_rem)
        dup_rem = input('Type the name of the columns you want to remove separated by a comma. Names should be exact: ')
        dup_rem = dup_rem.split(',')
        dup_rem = [x.strip() for x in dup_rem]
    else:
        print('No duplicate columns found.')
        dup_rem = []
    print('Removing duplicate columns from table')
    dedup_table = tt.remove_duplicates(a1, dup_rem)
    deduped_tbl = tt.create_df(dedup_table)
    deduped_mem = tt.create_in_memory_csv(deduped_tbl)
    print('Creating comparison agent')
    a2 = tt.create_agent([sys.argv[1], deduped_mem])
    print('Mapping columns from table 2 to table 1 and reformatting data.')
    sim_cols = tt.compare_tables(a2)
    cleaned_table = tt.rename_prune_table(a2, sim_cols)
    cleaned_mem = tt.create_in_memory_csv(tt.create_df(cleaned_table))
    a3 = tt.create_agent([sys.argv[1], cleaned_mem])
    final_dict = tt.reformat_columns(a3)
    final_dict = tt.extract_text_between_brackets(final_dict)
    print(final_dict)
    final_df = tt.create_df(final_dict)
    final_df.to_csv(sys.argv[4])
    print(f'Successfully transformed data. Saving as CSV as: {sys.argv[4]}')




    





    

    
