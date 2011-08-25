class CreatePeople < ActiveRecord::Migration
  def self.up
    create_table :people do |t|
      t.string :first_name
      t.string :last_name
      t.string :title
      t.string :level
      t.string :room
      t.string :image
      
      t.timestamps
    end
    
    add_index :people, [:last_name, :first_name], :unique => true
  end

  def self.down
    drop_table :people
  end
end
